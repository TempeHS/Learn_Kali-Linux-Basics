# Advanced CTF Tools

This repository includes several automated Python scripts in the `tools/` directory. These are designed to save you time during competitions by automating tedious processes, such as iterative decoding, binary searches for SQL injection, or generating custom wordlists.

> [!NOTE]
> Some scripts require third-party libraries. If you get an import error (for example, missing `PIL` or `requests`), check the comment at the top of the script or install the required system package (e.g., `sudo apt install python3-pil`).

---

## 1. Multiple Extraction: `ctf_peel.py`

When a flag is encoded multiple times (e.g., Base64 -> Hex -> Rot13 -> Base32), doing it by hand in CyberChef is slow. `ctf_peel.py` automatically detects and peels away layers of encoding and compression until it finds a flag.

**Usage:**

```bash
# Peel an encoded text file
python3 tools/ctf_peel.py challenge_file.txt

# Peel with a specific flag prefix to stop at
python3 tools/ctf_peel.py challenge.bin --flag-regex "pecan\{.*?\}"
```

**Supported Layers:** Gzip, Zlib, Bzip2, Base16/32/64/85, URL encoding, Hex, Binary, Rot13, Morse, and Single-byte XOR.

---

## 2. Multi-byte XOR Dragging: `xor_multibyte.py`

Many basic cryptography challenges use a repeating multi-byte key (e.g., a 4-character key like "pass"). If you know what the plaintext _should_ start with (the "crib"), you can automatically drag that crib across the ciphertext to reveal the key.

**Usage:**

```bash
# Provide the hex-encoded ciphertext and the known crib (e.g. "pecan{")
python3 tools/xor_multibyte.py "442e3a1f1a0d33...<long hex>..." "pecan{"
```

The script will slide `pecan{` across the ciphertext and print out potential matching key parts.

---

## 3. Basic RSA Automator: `rsa_toolkit.py`

If you are given an RSA public key (`n` and `e`) and a ciphertext (`c`), your only hope of decrypting it is if `n` is vulnerable (small or uses reused primes). This script queries the public FactorDB API to automatically check if `n` is factored, and if so, automates calculating the private key `d` to extract the plaintext.

**Usage:**

```bash
# python3 tools/rsa_toolkit.py <n> <e> <c>
python3 tools/rsa_toolkit.py 3233 17 2790
```

---

## 4. Custom Password Mangler: `mangler.py`

When provided with a target (like a fictional company named "Megacorp"), basic wordlists like Rockyou might fail. You need a targeted list. `mangler.py` takes a file of base words and generates an expansive dictionary by changing cases, converting text to leetspeak, and appending common combinations of years and symbols.

**Usage:**

1. Create a `basewords.txt` file containing your target words:
   ```text
   megacorp
   admin
   sysadmin
   ```
2. Run the mangler:
   ```bash
   python3 tools/mangler.py basewords.txt
   ```
3. A `mangled_wordlist.txt` will be created with hundreds of permutations (e.g., `M3gac0rp2024!`) ready to be plugged into John the Ripper or Hydra.

---

## 5. Boolean Blind SQLi Automator: `blind_sqli.py`

When an application is vulnerable to SQL injection but doesn't return any database output to the screen, you must extract data character-by-character by asking True/False questions (e.g., "Is the first letter of the password structurally greater than 'M'?").

`blind_sqli.py` is a _template_ that performs a fast Binary Search.

**Setup:**
You must edit the `URL`, the `TRUE_STRING` (the text on the page that confirms your query was True), and the `params=` parameter in the `check_truth()` function to match your specific web challenge before running it.

**Usage:**

```bash
python3 tools/blind_sqli.py 'SELECT version()'
```

---

## 6. LSB RGB Steganography Extractor: `lsb_extractor.py`

Hidden text and files are often tucked into the Least Significant Bit (LSB) of an image's Red, Green, and Blue pixels. While tools like `steghide` rely on headers and passwords, a raw LSB extractor pulls the exact bits and converts them straight back into bytes.

**Setup:**
Requires the Pillow image library. In Kali, install it with `sudo apt install python3-pil`.

**Usage:**

```bash
python3 tools/lsb_extractor.py secret_image.png
```

## This will carve out the data into an `lsb_extracted.bin` file and simultaneously check the first few kilobytes to see if a plain-text flag is immediately readable.

## 7. DNS Recon & Enumerator: `dns_enum.py`

In web and network CTFs, finding hidden subdomains (like `dev.megacorp.com`) is critical for finding vulnerable targets. A **Zone Transfer (AXFR)** is a misconfiguration where a DNS server dumps its entire directory to anyone who asks. If AXFR fails, the next best step is brute-forcing subdomains from a list.

**Setup:**
Requires `dnspython`. In Kali, install it with `sudo apt install python3-dnspython`.

**Usage:**

```bash
# 1. Attempt a Zone Transfer (AXFR) to dump all records
python3 tools/dns_enum.py target_domain.com

# 2. Attempt a Zone Transfer, and if it fails, brute-force subdomains
python3 tools/dns_enum.py target_domain.com -w /usr/share/wordlists/dirb/common.txt
```
