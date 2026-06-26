# Lesson 02 — Encoding, Decoding & CyberChef

Lots of CTF flags are not _hidden_ — they're just **encoded**. Encoding scrambles
text into another format (it is **not** encryption — there's no secret key). Your
job is to recognise the format and reverse it. The best tool for this is
**[CyberChef](https://gchq.github.io/CyberChef/)**, "the Cyber Swiss Army Knife".

> [!IMPORTANT]
> Practise only on your own data and the PECAN+ practice challenges.
> See [Lesson 00](00-ethics-and-safety.md).

## Learning goals

- Tell the difference between encoding and encryption.
- Recognise Base64, hex, binary, URL encoding and ROT13 on sight.
- Build a CyberChef "recipe" and reproduce it in the terminal.

## Part A — Spot the encoding

| Looks like…                                  | Probably is…       |
| -------------------------------------------- | ------------------ |
| `cGVjYW57...}` ends in `=` or letters+digits | **Base64**         |
| `70 65 63 61 6e` (pairs of 0-9 a-f)          | **Hex**            |
| `01110000 01100101` (only 0s and 1s)         | **Binary**         |
| `pecan%7Bhi%7D` (`%` codes)                  | **URL encoding**   |
| `crpna{...}` (looks like a flag but shifted) | **ROT13 / Caesar** |

## Part B — CyberChef (the visual way)

1. Open **https://gchq.github.io/CyberChef/**.
2. Paste the encoded text into the **Input** box (top right).
3. From **Operations** (left), drag **From Base64** into the **Recipe** (middle).
4. The **Output** (bottom right) updates instantly.
5. Stuck? Drag the **Magic** operation — it auto-detects encodings and even
   suggests a full recipe. Tick "Intensive mode" for layered encodings.

> CyberChef recipes can be _chained_: e.g. **From Base64 → From Hex → ROT13** all
> in one go. This is perfect for "encoded twice" challenges.

## Part C — Reproduce it in the terminal

Proving you can do it without the GUI cements the skill.

### If CyberChef feels confusing, use this simple fallback

When a challenge gives you a file/executable and you are stuck:

1. Pull readable text first with `strings`.
2. Look for Base64-looking chunks (letters/digits/`+`/`/`/`=`).
3. Decode candidates one by one with `base64 -d`.

Example workflow:

```bash
strings challenge_file | grep -E "[A-Za-z0-9+/=]{16,}"
echo "cGVjYW57aGVsbG99" | base64 -d
```

If the output is still unreadable, it may be encoded again. Try another step
such as hex decode or ROT13.

```bash
# Base64
echo -n "pecan{hello}" | base64
```

Expected output:

```
cGVjYW57aGVsbG99
```

```bash
echo -n "cGVjYW57aGVsbG99" | base64 -d
```

Expected output:

```
pecan{hello}
```

```bash
# Hex  ->  text   (-r reverse, -p plain)
echo -n "70 65 63 61 6e" | xxd -r -p
```

Expected output:

```
pecan
```

```bash
# text -> hex
echo -n "pecan" | xxd -p
```

Expected output:

```
706563616e
```

```bash
# ROT13 (shift letters by 13)
echo "Uryyb" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Expected output:

```
Hello
```

```bash
# Base32
echo -n "pecan" | base32
```

Expected output:

```
OBSWGYLO
```

## ✅ Challenge

1. **Do:** Decode `cGVjYW57YzBkZWR9` with CyberChef **and** the terminal.
2. **Verify:** Confirm your decoded output matches the `pecan{...}` flag format.
3. **Explain:** State why this example is encoding rather than encryption.
4. **Practice:** Complete **Cryptography → _Encoded_** at
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 03 — Cryptography Basics](03-cryptography.md)
