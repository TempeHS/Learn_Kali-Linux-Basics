# Lesson 03 — Cryptography Basics

Where encoding (Lesson 02) has no key, **cryptography** scrambles data with a
**key** so only someone with the key can read it. In CTFs you'll meet classic
ciphers (Caesar, XOR), hashes (one-way fingerprints) and real ciphers (AES).

> [!IMPORTANT]
> Only decrypt data you own or that a challenge gives you.
> See [Lesson 00](00-ethics-and-safety.md).

## Learning goals

- Break a Caesar cipher by trying all shifts.
- Understand XOR and one-time keys.
- Hash data and recognise hash types.
- Encrypt/decrypt a file with `openssl` (AES).

## Part A — Caesar / ROT (shift ciphers)

ROT13 is a Caesar cipher with shift 13. A general trick is to brute-force all 25
shifts and read the one that makes sense:

```bash
python3 - <<'PY'
ct = "Khoor"
for s in range(26):
    out = "".join(
        chr((ord(c) - base + s) % 26 + base) if c.isalpha() else c
        for c in ct
        for base in [65 if c.isupper() else 97]
    )
    print(f"shift {s:2}: {out}")
PY
```

Expected output (the readable line, shift 23 reverses a shift-3 Caesar):

```
shift 23: Hello
```

> In CyberChef this is the **ROT13 Brute Force** operation — much easier!

## Part B — XOR

XOR with a single byte is a classic beginner cipher. CyberChef's **XOR Brute
Force** tries every key for you. In the terminal you can XOR with Python:

```bash
python3 -c "print(bytes([b ^ 0x42 for b in b'\x32\x27\x21\x23\x2c']).decode())"
```

Expected output:

```
pecan
```

## Part C — Hashing (one-way fingerprints)

A hash always gives the same output for the same input, but you can't reverse it.

```bash
echo -n "password123" | md5sum
```

Expected output:

```
482c811da5d5b4bc6d497ffa98491e38  -
```

```bash
echo -n "secret" | sha256sum
```

Expected output:

```
2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b  -
```

```bash
# openssl gives the same hash, different formatting
echo -n "secret" | openssl dgst -sha256
```

Expected output:

```
SHA2-256(stdin)= 2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b
```

## Part D — Real encryption with AES

```bash
echo -n "pecan{crypto}" > msg.txt

# Encrypt (you choose the password after pass:)
openssl enc -aes-256-cbc -pbkdf2 -pass pass:mykey -in msg.txt -out msg.enc

# Decrypt
openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:mykey -in msg.enc
```

Expected output of the decrypt step:

```
pecan{crypto}
```

## ✅ Challenge

1. The string `pecan` was Caesar-shifted to `ujhfs` (shift 5). Use CyberChef _ROT13 Brute
   Force_ on `crpna{f1ggvat}` and read the flag.
2. Hash your own name with `sha256sum`. Is the output always 64 hex characters?
3. Try **Cryptography → _Take note_** and **_Climbing_** on
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 04 — OSINT & the Wayback Machine](04-osint-wayback.md)
