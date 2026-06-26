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

## Common ciphers quick table

Use this as a fast "what am I looking at?" guide during CTF challenges.

| Cipher / format               | What it is                            | Typical clue in challenge data                          | First thing to try                             |
| ----------------------------- | ------------------------------------- | ------------------------------------------------------- | ---------------------------------------------- |
| Caesar / ROT13                | Letters shifted by a fixed amount     | Text still looks word-like but wrong (`crpna`, `uryyb`) | CyberChef `ROT13 Brute Force` or `tr`          |
| Vigenere                      | Caesar with a repeating keyword       | Looks like random letters; hint mentions a "key word"   | CyberChef `Vigenere Decode` (test likely keys) |
| Atbash                        | Alphabet mirrored (`a<->z`, `b<->y`)  | Short weird text; often in beginner crypto/re puzzles   | CyberChef `Atbash`                             |
| Rail Fence                    | Letters rearranged in zig-zag rows    | No symbols, but letters are scrambled by position       | CyberChef `Rail Fence Cipher Decode`           |
| Affine                        | Math-based substitution over alphabet | Challenge mentions `ax + b` or "mod 26"                 | CyberChef `Affine Cipher Brute Force`          |
| XOR (single-byte)             | Each byte combined with a key byte    | Non-printable bytes / hex, hint says XOR                | CyberChef `XOR Brute Force` or Python          |
| Base64 (encoding, not cipher) | Text encoded to a transferable format | `A-Za-z0-9+/` and maybe trailing `=`                    | `base64 -d` or CyberChef `From Base64`         |

> Tip: many CTF tasks are layered. Decode one step, then re-check the output
> with this table again.

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

## Part E — How to solve "climbing" cipher challenges

Some CTF crypto tasks get harder in steps ("climbing"): decode layer 1, then
layer 2, then layer 3. Treat them like a staircase.

Use this order each time:

1. Check if it looks like Base64 (`A-Za-z0-9+/` with possible `=` at the end).
2. If not, check hex (`0-9a-f` pairs) or binary (`0` and `1` only).
3. If it looks like shifted text, brute-force Caesar/ROT.
4. Repeat until the result becomes readable text/flag.

Quick terminal ladder example:

```bash
# Step 1: decode Base64
echo "Y3JwbmF7ZjFnZ3ZhdH0=" | base64 -d

# Step 2: if it now looks shifted, try ROT13
echo "crpna{f1ggvat}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Expected final style of output:

```
pecan{...}
```

In CyberChef, this is just a recipe chain:

- `From Base64` -> `ROT13` (or `ROT13 Brute Force` if unsure).

## ✅ Challenge

1. **Do:** Use CyberChef _ROT13 Brute Force_ on `crpna{f1ggvat}` and recover the flag.
2. **Verify:** Hash your own name with `sha256sum` and confirm it is 64 hex characters.
3. **Explain:** Describe why hashing is one-way while AES decryption is reversible.
4. **Practice:** Complete **Cryptography → _Take note_** and **_Climbing_** on
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 04 — OSINT & the Wayback Machine](04-osint-wayback.md)
