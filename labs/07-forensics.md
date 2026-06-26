# Lesson 07 — Forensics

Digital **forensics** is examining files and data to work out what happened — the
detective work of cyber security. CTF forensics challenges hand you a mystery
file, a disk image or a captured network conversation (a **packet capture**, or
`.pcap`) and ask you to recover a hidden flag.

> [!IMPORTANT]
> Only examine files a challenge gives you or that you created.
> See [Lesson 00](00-ethics-and-safety.md).

## Learning goals

- Identify a file's _real_ type (not just its extension).
- Read raw bytes and spot "magic numbers".
- Carve embedded files out of a blob.
- Read a packet capture with `tshark`.

## Part A — What is this file, really?

Extensions lie. `file` reads the bytes and tells you the truth:

```bash
convert -size 8x8 xc:red PNG:mystery
file mystery
```

Expected output:

```
mystery: PNG image data, 8 x 8, 1-bit colormap, non-interlaced
```

## Part B — Read the raw bytes

The first few bytes of a file (its **magic number**) reveal its type. View them
as a hexdump:

```bash
xxd mystery | head -2
```

Expected output (starts with the PNG signature `89 50 4e 47` = `.PNG`):

```
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0008 0000 0008 0100 0000 00d3 10df  ................
```

Common magic numbers to memorise:

| Bytes         | File             |
| ------------- | ---------------- |
| `89 50 4E 47` | PNG              |
| `FF D8 FF`    | JPEG             |
| `50 4B 03 04` | ZIP / docx / apk |
| `25 50 44 46` | PDF (`%PDF`)     |

## Part C — Carve embedded files

`binwalk` finds files hidden inside other files; `foremost` rebuilds them.

```bash
echo "pecan{carved}" | gzip > hidden.gz
cat mystery hidden.gz > evidence.png
binwalk evidence.png
```

Expected output (note the `gzip` entry):

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 8 x 8, ...
343           0x157           gzip compressed data, ...
```

Extract what was found:

```bash
binwalk -e evidence.png          # auto-extract into _evidence.png.extracted/
```

## Part D — Network captures (.pcap)

CTF "you've captured some traffic" challenges give you a `.pcap`. Read it with
`tshark` (the command-line Wireshark):

```bash
# Show only HTTP packets
tshark -r capture.pcap -Y http

# List every URL that was requested
tshark -r capture.pcap -Y http -T fields -e http.request.full_uri

# Hunt for a flag across the whole capture
tshark -r capture.pcap -T fields -e data.text 2>/dev/null | grep -i pecan
```

> No capture file yet? You'll get one in **Forensics → _ABC company_**. You can
> also capture your own traffic with `sudo tcpdump -w mycapture.pcap`.

## Part E — Memory forensics triage (quick beginner method)

Some CTF forensics tasks give a RAM dump (`.raw`, `.mem`, `.dmp`) instead of a
normal file. Start with a fast triage pass before deep tooling.

Quick reference: [Memory dump triage (quick wins)](../CHEATSHEET.md#memory-dump-triage-quick-wins).

```bash
# Confirm what kind of dump you have
file memory.raw

# Pull likely clues (flags, tokens, hostnames, commands)
strings -n 8 memory.raw | grep -iE "pecan\{|flag\{|token|password|http" | head -n 30
```

If the challenge hints at processes, network activity, or command history,
memory frameworks (for example Volatility) can be used for deeper analysis.
But in many beginner CTFs, plain `strings` already reveals enough to pivot.

Triage mindset:

1. Extract obvious text clues.
2. Group clues by theme (credentials, URLs, commands, usernames).
3. Use each clue to search related artifacts (pcap, disk files, web pages).

## ✅ Challenge

1. **Do:** Run `file` on something in `/bin` (for example, `/bin/ls`) and identify its type.
2. **Verify:** Carve the gzip out of `evidence.png` with `binwalk -e` and confirm you recovered the hidden content.
3. **Explain:** Create `memory.raw`, run the triage `strings` command, and explain one clue type you found.
4. **Practice:** Complete **Forensics → _3D flag_**, **_ABC company_** (pcap), and **_HackersAttack_** at
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 08 — Reverse Engineering Basics](08-reverse-engineering.md)
