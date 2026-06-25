# Lesson 08 — Reverse Engineering & Binary Exploitation Basics

**Reverse engineering** (RE) means taking a finished program apart to understand
how it works — and, in a CTF, to recover a secret it's hiding. You don't need to
be a programmer to start: the easiest flags fall to `strings` before you ever
open a disassembler.

> [!IMPORTANT]
> Only analyse binaries from a challenge or that you compiled yourself.
> See [Lesson 00](00-ethics-and-safety.md).

## Learning goals

- Identify a binary's type and architecture.
- Pull readable text and secrets out of a binary.
- Read a disassembly and explore functions with `radare2`.
- Understand the core binary exploitation workflow used in CTF pwn challenges.

## Part A — Identify the binary

```bash
file -L /usr/bin/python3
```

Expected output (an ELF is a Linux executable):

```
/usr/bin/python3: ELF 64-bit LSB ... x86-64 ...
```

```bash
objdump -f /usr/bin/python3 | head -4
```

Expected output:

```
/usr/bin/python3:     file format elf64-x86-64
architecture: i386:x86-64, flags 0x00000112:
EXEC_P, HAS_SYMS, D_PAGED
```

## Part B — Easy wins first: strings

Most beginner RE challenges store the flag as plain text. Always try this first:

```bash
strings /usr/bin/python3 | grep -i "version" | head -3
```

In a real challenge you'd run `strings ./program | grep -i pecan`.

### Important beginner workflow: strings first, then decode

A lot of binaries hide a flag as encoded text, not plain text. Use this exact
flow:

1. Run `strings` on the executable.
2. Find suspicious long text chunks.
3. If a chunk looks like Base64, decode it.

```bash
# 1) Pull readable text from the executable
strings ./program > out.txt

# 2) Find possible Base64 chunks
grep -E "[A-Za-z0-9+/=]{16,}" out.txt

# 3) Decode one candidate
echo "cGVjYW57aGVsbG99" | base64 -d
```

Expected decode output:

```
pecan{hello}
```

If decode output still looks scrambled, it is probably layered (for example:
Base64 then ROT13). Send that output to CyberChef and chain operations.

## Part C — Disassemble

`objdump -d` turns machine code back into assembly. You're looking for compared
strings, suspicious constants or function names:

```bash
objdump -d /usr/bin/python3 | head -20    # press q if you pipe to less
```

You'll see lines like `mov`, `cmp`, `call` — the CPU instructions the program runs.

## Part D — Interactive analysis with radare2

`radare2` is a full reverse-engineering toolkit. Confirm it's installed:

```bash
radare2 -v | head -1
```

Expected output (version may differ):

```
radare2 6.0.5 0 @ linux-x86-64
```

A typical session (a sample binary `./crackme`):

```bash
radare2 -A ./crackme      # -A analyses the whole binary on load
```

Then at the `[0x...]>` prompt:

| Command             | What it does                                                 |
| ------------------- | ------------------------------------------------------------ |
| `afl`               | **a**nalyse **f**unction **l**ist — show all functions       |
| `s main` then `pdf` | seek to `main` and **p**rint **d**isassembly of **f**unction |
| `izz ~pecan`        | search all strings for `pecan`                               |
| `q`                 | quit                                                         |

> Prefer a GUI? **Ghidra** does the same job with a graphical decompiler. For
> beginner CTFs, `strings` + `radare2` is usually enough.

## Part E — Binary exploitation core skills (pwn)

Reverse engineering tells you what a binary does; binary exploitation (pwn)
focuses on making it do something unintended.

### 1. Protections check (concept)

Modern binaries may include protections like canaries, NX and PIE. These change
your exploit strategy.

### 2. Debugging workflow with gdb

Use gdb to inspect execution state and memory:

```bash
gdb -q /bin/ls -ex "info files" -ex "quit" | head -n 8
```

Expected output includes:

```
Symbols from "/bin/ls".
```

### 3. Build offsets with a cyclic pattern

CTF pwn workflows often use generated patterns to find exact crash offsets:

```bash
python3 - <<'PY'
import string
alphabet = string.ascii_lowercase
pattern = "".join(a + b + c for a in alphabet for b in alphabet for c in alphabet)
print(pattern[:24])
PY
```

Expected output:

```
aaaaabaacaadaaeaafaagaah
```

### 4. Endianness and packed addresses

Most Linux CTF binaries are little-endian. That means addresses are written
least-significant byte first.

```bash
python3 -c "import struct; print(struct.pack('<I', 0x41424344).hex())"
```

Expected output:

```
44434241
```

This is the same idea used when building payloads for stack overflows.

### 5. Core pwn concepts to learn next

- Stack buffer overflow and instruction pointer control.
- Return-to-win and return-oriented programming (ROP).
- Bypassing ASLR/NX/canaries with leaks and gadgets.
- Automating exploitation with Python scripts.

## ✅ Challenge

1. Run `file` on `/bin/ls` and `/usr/bin/python3`. Are they both ELF?
2. Use `strings ... | grep` to find the Python version string in the binary.
3. Run the gdb `info files` command and record one section name you see.
4. Generate a 24-byte cyclic pattern and explain why offsets matter in pwn.
5. Try **Reverse Engineering → _Love letter_** at
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 09 — Network Scanning with Nmap](09-network-scanning-nmap.md)
