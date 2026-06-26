# Lesson 06 — Steganography

**Steganography** is hiding data _inside_ something ordinary — a flag tucked into
an image, a message buried in an audio file. Unlike cryptography (which hides the
_meaning_), steganography hides the _existence_ of the message. CTFs love it.

> [!IMPORTANT]
> Only inspect files provided by a challenge or that you created.
> See [Lesson 00](00-ethics-and-safety.md).

## Learning goals

- Read hidden text and metadata from an image.
- Spot files embedded inside other files.
- Extract a payload hidden with `steghide`.

## Always start with these three

```bash
# 1. Metadata — flags hide in Comment / Artist / GPS fields
exiftool suspect.png

# 2. Plain text inside the file
strings suspect.png | grep -i pecan

# 3. Files hidden inside the file
binwalk suspect.png
```

## Try it for real (create, then crack)

Make a test image and hide a comment in it:

```bash
convert -size 64x64 xc:skyblue suspect.png
exiftool -overwrite_original -Comment="pecan{exif_hunter}" suspect.png
exiftool -Comment suspect.png
```

Expected output:

```
Comment                         : pecan{exif_hunter}
```

Hide plain text and find it with `strings`:

```bash
printf '\x89PNG\x00pecan{in_the_bytes}\x00' > blob.png
strings blob.png | grep pecan
```

Expected output:

```
pecan{in_the_bytes}
```

## steghide — password-protected hiding

`steghide` embeds a file inside a BMP/JPEG/WAV, optionally with a passphrase.

```bash
# Make a cover image and a secret
convert -size 200x200 xc:gray BMP3:cover.bmp
echo "pecan{stego_master}" > flag.txt

# Embed the secret (passphrase: hunter2)
steghide embed -cf cover.bmp -ef flag.txt -sf out.bmp -p hunter2 -q

# Later: extract it back out
steghide extract -sf out.bmp -p hunter2 -xf revealed.txt -q
cat revealed.txt
```

Expected output:

```
pecan{stego_master}
```

> No password? Try an empty one (`-p ""`) or common words. CTF stego passwords
> are often hinted at in the challenge text.

## binwalk — carve embedded files

If a file _contains_ another file (e.g. a zip glued to a PNG):

```bash
echo "pecan{hidden_zip}" | gzip > secret.gz
cat cover.bmp secret.gz > combo.bmp
binwalk combo.bmp
```

Expected output (note the `gzip` line):

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PC bitmap, Windows 3.x format...
...           ...             gzip compressed data
```

Extract everything binwalk finds with `binwalk -e combo.bmp`.

## ✅ Challenge

1. **Do:** Hide your initials in an image `Comment` field and read them back.
2. **Verify:** Extract the embedded gzip with `binwalk -e` and confirm the output.
3. **Explain:** State which tool found metadata clues vs embedded-file clues.
4. **Practice:** Complete **Steganography → _Head in the clouds_**,
   **_Matchy matchy_** and **_The guy_** (hint: EXIF) at
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 07 — Forensics](07-forensics.md)
