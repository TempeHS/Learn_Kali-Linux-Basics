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
- Look up cracked password hashes with CrackStation.
- Encrypt/decrypt a file with `openssl` (AES).
- Understand the basics of RSA and why factoring breaks it.

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

### Better tool for shift ciphers: cryptii

For Caesar/ROT work, [cryptii Caesar Cipher](https://cryptii.com/pipes/caesar-cipher/)
is easier than CyberChef: paste the ciphertext on the left, then drag the
**shift** slider and watch the plaintext update live. When the output reads as
English, note the shift number — that is the key.

> Use **cryptii** for Caesar/ROT/Atbash-style puzzles, and **CyberChef** when you
> need to chain several operations together (e.g. `From Base64` -> `ROT13` -> `From Hex`).

## Common ciphers quick table

Use this as a fast "what am I looking at?" guide during CTF challenges.

| Cipher / format               | What it is                            | Typical clue in challenge data                          | First thing to try                                                |
| ----------------------------- | ------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------- |
| Caesar / ROT13                | Letters shifted by a fixed amount     | Text still looks word-like but wrong (`crpna`, `uryyb`) | [cryptii Caesar Cipher](https://cryptii.com/pipes/caesar-cipher/) |
| Vigenere                      | Caesar with a repeating keyword       | Looks like random letters; hint mentions a "key word"   | CyberChef `Vigenere Decode` (test likely keys)                    |
| Atbash                        | Alphabet mirrored (`a<->z`, `b<->y`)  | Short weird text; often in beginner crypto/re puzzles   | CyberChef `Atbash`                                                |
| Rail Fence                    | Letters rearranged in zig-zag rows    | No symbols, but letters are scrambled by position       | CyberChef `Rail Fence Cipher Decode`                              |
| Affine                        | Math-based substitution over alphabet | Challenge mentions `ax + b` or "mod 26"                 | CyberChef `Affine Cipher Brute Force`                             |
| XOR (single-byte)             | Each byte combined with a key byte    | Non-printable bytes / hex, hint says XOR                | CyberChef `XOR Brute Force` or Python                             |
| Base64 (encoding, not cipher) | Text encoded to a transferable format | `A-Za-z0-9+/` and maybe trailing `=`                    | `base64 -d` or CyberChef `From Base64`                            |

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

A hash always gives the same output for the same input. Secure hashes are
designed to be one-way: there is no decryption key, though weak inputs can be
guessed and compared with their hashes.

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

### Cracking password hashes with CrackStation

You cannot reverse a hash, but you _can_ look it up. [CrackStation](https://crackstation.net/)
holds a huge table of pre-computed hashes for leaked and dictionary passwords.
Paste a hash (MD5, SHA-1, SHA-256, NTLM…) and it returns the password if that
password is in the table.

Try it with the MD5 from above:

```
482c811da5d5b4bc6d497ffa98491e38
```

CrackStation returns `password123`. Now hash a long random passphrase of your
own and paste that hash in. A genuinely random passphrase is unlikely to be in
CrackStation's lookup tables.

> [!IMPORTANT]
> Only submit hashes from your own systems or from a challenge you are allowed
> to solve. Pasting real user hashes into a public website leaks them.

> [!NOTE]
> This is why real sites add a **salt** (random per-user text) before hashing:
> the same password then produces a different hash for every user, so lookup
> tables like CrackStation stop working.

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

AES is **symmetric**: the same password locks and unlocks the message. That is a
problem if you have never met the other person — how do you send them the
password safely? RSA solves exactly that.

## Part E — Basics of RSA (public-key cryptography)

RSA uses **two** keys: a **public key** anyone may have (used to encrypt) and a
**private key** you keep secret (used to decrypt). You can publish the public key
on the internet and still receive messages only you can read.

How the keys are built:

1. Pick two large prime numbers, `p` and `q`.
2. Multiply them: `n = p * q`. This `n` is the **modulus** and is public.
3. Pick a public exponent `e` (almost always `65537`). `(n, e)` is the public key.
4. Use `p` and `q` to calculate the private exponent `d`. `(n, d)` is the private key.

Encrypting a number `m` is `c = m^e mod n`. Decrypting is `m = c^d mod n`.

### Why RSA is secure — and how CTFs break it

Multiplying two primes is easy. Going backwards — **factoring** `n` back into `p`
and `q` — is impossibly slow when the primes are hundreds of digits long. Real
RSA uses a 2048-bit `n`.

CTF challenges cheat by handing you a **small** `n`. If you can factor it, you can
rebuild `d` and decrypt everything. Paste `n` into
[WolframAlpha's factoring calculator](https://www.wolframalpha.com/calculators/factoring-calculator/)
and it returns the prime factors.

Try it with `n = 3233`:

```
3233 = 53 × 61
```

So `p = 53` and `q = 61`. With `e = 17` you can finish the maths in Python:

```bash
python3 - <<'PY'
p, q, e = 53, 61, 17
n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)          # private exponent
c = 2790                     # the intercepted ciphertext number
print("d =", d)
print("m =", pow(c, d, n))   # decrypt
PY
```

Expected output:

```
d = 2753
m = 65
```

`65` is the ASCII code for `A` — the original message.

> Rule of thumb: if `n` is small enough for WolframAlpha to factor, factoring is
> the intended solution. If `n` is huge, the challenge wants a _different_
> weakness (a tiny `e`, reused primes between two keys, or a leaked `d`).

## Part F — How to solve "climbing" cipher challenges

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

1. **Do:** Use [cryptii Caesar Cipher](https://cryptii.com/pipes/caesar-cipher/)
   (or CyberChef _ROT13 Brute Force_) on `crpna{f1ggvat}` and recover the flag.
2. **Verify:** Hash your own name with `sha256sum` and confirm it is 64 hex characters.
3. **Do:** Paste the MD5 `5f4dcc3b5aa765d61d8327deb882cf99` into
   [CrackStation](https://crackstation.net/) and find the password. Then hash a
   12-character random passphrase and see whether CrackStation can find it.
4. **Do:** Factor `n = 8051` with the
   [WolframAlpha factoring calculator](https://www.wolframalpha.com/calculators/factoring-calculator/)
   and write down `p` and `q`.
5. **Explain:** Describe why hashing is one-way while AES decryption is reversible,
   and why RSA needs _two_ keys where AES needs only one.
6. **Practice:** Complete **Cryptography → _Take note_** and **_Climbing_** on
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 04 — OSINT & the Wayback Machine](04-osint-wayback.md)
