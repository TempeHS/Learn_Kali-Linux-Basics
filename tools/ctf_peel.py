#!/usr/bin/env python3
"""
ctf_peel.py - Iteratively identify and strip encoding layers from a CTF blob.

Works on ANY file type: .txt, .sh, .py, .bin, .dat, images, raw stdin.
Files are always opened in binary mode; text decoders simply skip
layers that aren't valid text.

Usage:
    python3 ctf_peel.py encoded.sh
    python3 ctf_peel.py payload.bin --max-depth 60
    cat blob | python3 ctf_peel.py
    python3 ctf_peel.py enc.txt --flag-regex 'HTB\\{.*?\\}' --save-layers out/
"""

import argparse
import base64
import binascii
import bz2
import codecs
import gzip
import lzma
import os
import re
import sys
import zlib
from urllib.parse import unquote_to_bytes

MAX_DEPTH_DEFAULT = 40
DEFAULT_FLAG_RE = r"(flag|ctf|htb|picoctf)\{[^}]{2,}\}"


# ---------- helpers ----------

def as_text(data: bytes):
    """Return str if data decodes to mostly-printable UTF-8, else None."""
    try:
        s = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not s.strip():
        return None
    printable = sum(1 for c in s if c.isprintable() or c in "\r\n\t")
    return s if printable / len(s) > 0.90 else None


def strip_ws(s: str) -> str:
    return re.sub(r"\s+", "", s)


def looks_like_flag(data: bytes, pattern: str) -> bool:
    t = as_text(data)
    return bool(t and re.search(pattern, t, re.IGNORECASE))


def printable_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    ok = sum(1 for b in data if 32 <= b <= 126 or b in (9, 10, 13))
    return ok / len(data)


# ---------- decoders (return bytes, or None if not applicable) ----------

def try_base64(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t)
    if len(s) < 8 or not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return None
    return base64.b64decode(s + "=" * (-len(s) % 4), validate=False) or None


def try_base64_url(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t)
    if len(s) < 8 or not re.fullmatch(r"[A-Za-z0-9_-]+={0,2}", s):
        return None
    if "-" not in s and "_" not in s:
        return None                      # plain base64 already covers it
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4)) or None


def try_base32(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t).upper()
    if len(s) < 8 or not re.fullmatch(r"[A-Z2-7]+={0,6}", s):
        return None
    return base64.b32decode(s + "=" * (-len(s) % 8)) or None


def try_base85(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t)
    if len(s) < 8:
        return None
    return base64.b85decode(s) or None


def try_ascii85(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t)
    if len(s) < 8:
        return None
    return base64.a85decode(s, adobe=s.startswith("<~")) or None


def try_base16(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t)
    if len(s) < 8 or len(s) % 2 or not re.fullmatch(r"[0-9a-fA-F]+", s):
        return None
    return binascii.unhexlify(s) or None


def try_hex_prefixed(data):
    t = as_text(data)
    if not t:
        return None
    tokens = re.findall(r"(?:0x|\\x)([0-9a-fA-F]{2})", t)
    if len(tokens) < 4:
        return None
    return bytes(int(h, 16) for h in tokens)


def try_decimal_bytes(data):
    t = as_text(data)
    if not t:
        return None
    tokens = [x for x in re.split(r"[\s,;]+", t.strip()) if x]
    if len(tokens) < 4 or not all(tok.isdigit() for tok in tokens):
        return None
    vals = [int(tok) for tok in tokens]
    if any(v > 255 for v in vals):
        return None
    return bytes(vals)


def try_octal_bytes(data):
    t = as_text(data)
    if not t:
        return None
    tokens = re.findall(r"\\([0-7]{2,3})", t)
    if len(tokens) < 4:
        return None
    vals = [int(o, 8) for o in tokens]
    if any(v > 255 for v in vals):
        return None
    return bytes(vals)


def try_binary(data):
    t = as_text(data)
    if not t:
        return None
    s = strip_ws(t)
    if len(s) < 16 or len(s) % 8 or not re.fullmatch(r"[01]+", s):
        return None
    return bytes(int(s[i:i + 8], 2) for i in range(0, len(s), 8))


def try_url(data):
    t = as_text(data)
    if not t or not re.search(r"%[0-9a-fA-F]{2}", t):
        return None
    out = unquote_to_bytes(t)
    return out if out != data else None


def try_html_entities(data):
    import html
    t = as_text(data)
    if not t or not re.search(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);", t):
        return None
    out = html.unescape(t).encode()
    return out if out != data else None


def try_rot13(data):
    t = as_text(data)
    if not t or not re.search(r"[A-Za-z]", t):
        return None
    return codecs.encode(t, "rot_13").encode()


def try_reversed(data):
    t = as_text(data)
    if not t:
        return None
    return t[::-1].encode()


def try_gzip(data):
    if not data.startswith(b"\x1f\x8b"):
        return None
    return gzip.decompress(data)


def try_zlib(data):
    if len(data) < 2 or data[0] != 0x78:
        return None
    return zlib.decompress(data)


def try_bz2(data):
    if not data.startswith(b"BZh"):
        return None
    return bz2.decompress(data)


def try_lzma(data):
    if not (data.startswith(b"\xfd7zXZ") or data.startswith(b"\x5d\x00\x00")):
        return None
    return lzma.decompress(data)


def try_raw_deflate(data):
    if printable_ratio(data) > 0.85:
        return None                      # looks like text, not deflate
    return zlib.decompress(data, -15)


def try_xor_single_byte(data):
    """Brute-force single-byte XOR; accept only if result is clean text."""
    if len(data) < 8:
        return None
    best, best_score = None, 0.0
    for key in range(1, 256):
        cand = bytes(b ^ key for b in data)
        sc = printable_ratio(cand)
        if sc > best_score:
            best, best_score = cand, sc
    return best if best_score > 0.97 else None


def try_morse(data):
    MORSE = {
        ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
        "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
        "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
        "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
        "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
        "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7",
        "---..": "8", "----.": "9",
    }
    t = as_text(data)
    if not t or "." not in t or not re.fullmatch(r"[.\-/\s]+", t.strip()):
        return None
    out = []
    for word in re.split(r"\s*/\s*|\s{3,}", t.strip()):
        for sym in word.split():
            if sym not in MORSE:
                return None
            out.append(MORSE[sym])
        out.append(" ")
    return "".join(out).strip().encode()


# Order matters: magic-byte / strict formats first, loose ones last.
DECODERS = [
    ("gzip",              try_gzip,          True),
    ("zlib",              try_zlib,          True),
    ("bzip2",             try_bz2,           True),
    ("lzma/xz",           try_lzma,          True),
    ("raw deflate",       try_raw_deflate,   True),
    ("binary (base2)",    try_binary,        False),
    ("morse code",        try_morse,         False),
    ("hex (0x/\\x)",      try_hex_prefixed,  False),
    ("octal escapes",     try_octal_bytes,   False),
    ("decimal bytes",     try_decimal_bytes, False),
    ("base16 (hex)",      try_base16,        False),
    ("base32",            try_base32,        False),
    ("base64",            try_base64,        False),
    ("base64url",         try_base64_url,    False),
    ("base85",            try_base85,        False),
    ("ascii85",           try_ascii85,       False),
    ("url/percent",       try_url,           False),
    ("html entities",     try_html_entities, False),
    ("rot13",             try_rot13,         False),
    ("single-byte XOR",   try_xor_single_byte, False),
    ("reversed string",   try_reversed,      False),
]


def preview(data: bytes, n: int = 120) -> str:
    t = as_text(data)
    if t is not None:
        return repr(t[:n].replace("\n", "\\n"))
    return repr(data[:n // 2]) + f"  <binary, {len(data)} bytes>"


def peel(data: bytes, max_depth: int, flag_regex: str, save_dir=None):
    seen = {data}
    chain = []

    print(f"[*] Input: {len(data)} bytes")
    print(f"[*] Layer 0: {preview(data)}\n")

    for depth in range(1, max_depth + 1):
        if looks_like_flag(data, flag_regex):
            print(f"[!] Flag pattern matched — stopping at depth {depth - 1}.")
            break

        progressed = False
        for name, fn, is_binary_format in DECODERS:
            try:
                out = fn(data)
            except Exception:
                continue
            if not out or out in seen:
                continue

            # Reject junk: text-based decoders must yield readable output
            # unless the result is a recognisable compressed stream.
            magic = out[:4]
            is_container = (magic.startswith(b"\x1f\x8b") or out[:1] == b"\x78"
                            or magic.startswith(b"BZh") or magic.startswith(b"\xfd7z"))
            if not is_binary_format and not is_container:
                if printable_ratio(out) < 0.90:
                    continue

            print(f"[+] Layer {depth}: {name}")
            print(f"    -> {preview(out)}\n")
            chain.append(name)
            seen.add(out)
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
                path = os.path.join(save_dir, f"layer_{depth:02d}_{name.split()[0]}.bin")
                with open(path, "wb") as fh:
                    fh.write(out)
            data = out
            progressed = True
            break

        if not progressed:
            print(f"[*] No further encoding recognised at depth {depth}. Done.")
            break
    else:
        print(f"[!] Hit max depth ({max_depth}); output may still be encoded.")

    print("=" * 64)
    print("Encoding chain (outermost -> innermost):")
    print("  " + (" -> ".join(chain) if chain else "(none detected)"))
    print("=" * 64)
    print("FINAL OUTPUT:")
    t = as_text(data)
    sys.stdout.write(t if t is not None else repr(data))
    print()

    m = re.search(flag_regex, t or "", re.IGNORECASE)
    if m:
        print(f"\n[FLAG] {m.group(0)}")
    return data, chain


def main():
    p = argparse.ArgumentParser(description="Auto-detect and peel CTF encoding layers.")
    p.add_argument("file", nargs="?", help="input file (any type); omit to read stdin")
    p.add_argument("--max-depth", type=int, default=MAX_DEPTH_DEFAULT)
    p.add_argument("--flag-regex", default=DEFAULT_FLAG_RE)
    p.add_argument("--save-layers", metavar="DIR", help="write each layer to DIR")
    args = p.parse_args()

    if args.file:
        if not os.path.isfile(args.file):
            sys.exit(f"error: no such file: {args.file}")
        with open(args.file, "rb") as fh:      # binary mode = any file type
            data = fh.read()
    else:
        data = sys.stdin.buffer.read()

    if not data:
        sys.exit("error: empty input")

    peel(data, args.max_depth, args.flag_regex, args.save_layers)


if __name__ == "__main__":
    main()
