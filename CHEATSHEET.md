# Kali Linux & CTF Cheat Sheet

A quick command reference for the [Kali Linux & CTF course](COURSE_PLAN.md).
Every entry shows the **command** and the **expected output** you should see in
this codespace, organised by the common CTF categories. Flags are shown in the
generic `flag{...}` format — real competitions use their own (`flag{}`, `CTF{}`,
etc.), so always check your event's rules.

> [!TIP]
> Outputs below were captured in this container. Yours may differ slightly
> (dates, IP latency, file sizes). Validate the whole sheet at any time with
> `python3 -m pytest -v`.

---

## 1. Linux command line

| Command                          | Expected output                                            |
| -------------------------------- | ---------------------------------------------------------- |
| `whoami`                         | `student`                                                  |
| `pwd`                            | `/home/student`                                            |
| `cat /etc/os-release \| head -1` | `PRETTY_NAME="Kali GNU/Linux Rolling"`                     |
| `ls -la`                         | a long listing including `.` and `..` and any hidden files |
| `grep -r "flag" .`               | every line in the current tree containing `flag`           |
| `find . -name "*.txt"`           | paths of all `.txt` files below the current folder         |
| `man nmap`                       | the Nmap manual (press `q` to quit)                        |

---

## 2. Encoding & decoding — CyberChef equivalents

Open [CyberChef](https://gchq.github.io/CyberChef/) and drag operations, or use
the terminal:

| Command                                      | Expected output              |
| -------------------------------------------- | ---------------------------- |
| `echo -n "flag{hello}" \| base64`            | `ZmxhZ3toZWxsb30=`           |
| `echo -n "ZmxhZ3toZWxsb30=" \| base64 -d`    | `flag{hello}`                |
| `echo -n "flag" \| base32`                   | `MZWGCZY=`                   |
| `echo -n "66 6c 61 67" \| xxd -r -p`         | `flag`                       |
| `echo -n "flag" \| xxd -p`                   | `666c6167`                   |
| `echo "Uryyb" \| tr 'A-Za-z' 'N-ZA-Mn-za-m'` | `Hello` (ROT13)              |
| `echo -n "ced5c5cd" \| xxd -r -p \| xxd`     | hex bytes shown as a hexdump |

> **CyberChef tip:** the **Magic** operation auto-detects layered encodings —
> paste the blob, drag _Magic_, and read the suggested recipe.

---

## 3. Cryptography & hashing

| Command                                                                    | Expected output                                                                     |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `echo -n "password123" \| md5sum`                                          | `482c811da5d5b4bc6d497ffa98491e38  -`                                               |
| `echo -n "secret" \| sha256sum`                                            | `2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b  -`               |
| `echo -n "secret" \| openssl dgst -sha256`                                 | `SHA2-256(stdin)= 2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b` |
| `openssl enc -aes-256-cbc -pbkdf2 -pass pass:key -in msg.txt -out msg.enc` | _(no output; creates `msg.enc`)_                                                    |
| `openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:key -in msg.enc`           | the original plaintext of `msg.txt`                                                 |

### Common ciphers quick guide

| Cipher / format                 | Typical clue                                        | First thing to try                     |
| ------------------------------- | --------------------------------------------------- | -------------------------------------- |
| Caesar / ROT13                  | text looks word-like but shifted (`uryyb`, `crpna`) | CyberChef `ROT13 Brute Force` or `tr`  |
| Vigenere                        | hint mentions a keyword; letters look random        | CyberChef `Vigenere Decode`            |
| Atbash                          | short weird text, substitution-style puzzle         | CyberChef `Atbash`                     |
| Rail Fence                      | letters scrambled by position/rows                  | CyberChef `Rail Fence Cipher Decode`   |
| Affine                          | hint includes `ax + b` or `mod 26`                  | CyberChef `Affine Cipher Brute Force`  |
| XOR (single-byte)               | bytes/hex look noisy; challenge says XOR            | CyberChef `XOR Brute Force`            |
| Base64 (encoding, not a cipher) | `A-Za-z0-9+/` with optional trailing `=`            | `base64 -d` or CyberChef `From Base64` |

> Tip: if one step produces new gibberish, it is probably layered. Decode one
> layer at a time and re-check the result.

---

## 4. OSINT & the Wayback Machine

| Command                                                                  | Expected output                                                                                                   |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `whois example.com \| grep -i registrar`                                 | the domain's registrar line(s)                                                                                    |
| `dig +short scanme.nmap.org`                                             | `45.33.32.156`                                                                                                    |
| `curl -s "http://archive.org/wayback/available?url=example.com"`         | `{"url": "example.com", "archived_snapshots": {"closest": {"status": "200", ... "timestamp": "20260620000127"}}}` |
| `curl -s "https://web.archive.org/web/2020/http://example.com/" \| head` | the HTML of the site **as it looked in 2020**                                                                     |

> **Wayback tip:** browse `https://web.archive.org/web/*/SITE` to see every saved
> snapshot — deleted pages, old emails and leaked flags often live in history.

---

## 5. Web reconnaissance & exploitation basics

| Command                                                                        | Expected output                                              |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `curl -s http://testphp.vulnweb.com/robots.txt`                                | `User-agent: *` and `Disallow:` lines (paths the site hides) |
| `curl -s URL \| grep -i "flag\|hidden\|TODO\|<!--"`                            | suspicious comments / hidden text in the page source         |
| `curl -sI URL`                                                                 | HTTP response headers (`Server:`, `X-Powered-By:`)           |
| `whatweb http://testphp.vulnweb.com`                                           | a one-line fingerprint of the site's tech stack              |
| `gobuster dir -u URL -w /usr/share/wordlists/dirb/common.txt`                  | discovered paths with `Status: 200/301`                      |
| `nikto -h URL`                                                                 | a list of potential web server issues                        |
| `curl -s "http://testphp.vulnweb.com/listproducts.php?cat=1%27" \| head -n 20` | SQL-related error text can indicate injectable input         |
| `sqlmap --version`                                                             | installed version string                                     |

---

## 6. Steganography

| Command                                                             | Expected output                                             |
| ------------------------------------------------------------------- | ----------------------------------------------------------- |
| `exiftool image.png`                                                | full metadata table; flags often hide in `Comment`/`Artist` |
| `exiftool -Comment image.png`                                       | `Comment                         : flag{exif}`              |
| `strings image.png \| grep flag`                                    | `flag{strings}` (plain text inside the file)                |
| `binwalk image.png`                                                 | a table of embedded files (e.g. `gzip compressed data`)     |
| `steghide extract -sf secret.jpg -p PASSWORD`                       | `wrote extracted data to "...".`                            |
| `steghide embed -cf cover.bmp -ef flag.txt -sf out.bmp -p PASSWORD` | `embedding "flag.txt" in "cover.bmp"... done`               |

---

## 7. Forensics

| Command                                                               | Expected output                                         |
| --------------------------------------------------------------------- | ------------------------------------------------------- |
| `file mystery`                                                        | the true file type, e.g. `PNG image data, 8 x 8, ...`   |
| `binwalk -e firmware.bin`                                             | extracts embedded files into `_firmware.bin.extracted/` |
| `foremost -i disk.img -o out/`                                        | carves files by signature into `out/`                   |
| `xxd capture.bin \| head`                                             | a hexdump of the first bytes (look for magic numbers)   |
| `tshark -r capture.pcap -Y http`                                      | the HTTP packets inside a capture file                  |
| `tshark -r capture.pcap -Y "http" -T fields -e http.request.full_uri` | every URL requested in the capture                      |

---

## 8. Reverse engineering & binary exploitation basics

| Command                                                                  | Expected output                             |
| ------------------------------------------------------------------------ | ------------------------------------------- |
| `file program`                                                           | `ELF 64-bit LSB executable, x86-64, ...`    |
| `strings program \| grep flag`                                           | any flag stored as plain text in the binary |
| `objdump -f program`                                                     | `architecture: i386:x86-64 ...` header info |
| `objdump -d program \| less`                                             | the full disassembly (press `q` to quit)    |
| `radare2 -v`                                                             | `radare2 6.0.5 0 @ linux-x86-64`            |
| `radare2 -A program` then `afl`                                          | analysis loaded; `afl` lists all functions  |
| `gdb -q /bin/ls -ex "info files" -ex "quit" \| head -n 8`                | includes `Symbols from "/bin/ls".`          |
| `python3 -c "import struct; print(struct.pack('<I', 0x41424344).hex())"` | `44434241` (little-endian)                  |

---

## 9. Network scanning

| Command                                 | Expected output                                  |
| --------------------------------------- | ------------------------------------------------ |
| `nmap -sn scanme.nmap.org`              | `Host is up` ping-scan result                    |
| `nmap -sT -Pn -p 22,80 scanme.nmap.org` | `22/tcp open ssh` and `80/tcp open http`         |
| `nmap -sV scanme.nmap.org`              | open ports **plus** the software version on each |
| `dig +short scanme.nmap.org`            | `45.33.32.156`                                   |

> [!NOTE]
> In Codespaces use **`-sT`** (TCP connect) scans — raw-packet scans need
> privileges the container doesn't have.

---

## 10. Passwords & hashes

| Command                                                                   | Expected output                           |
| ------------------------------------------------------------------------- | ----------------------------------------- |
| `hashid 482c811da5d5b4bc6d497ffa98491e38`                                 | `[+] MD5` (among the guessed types)       |
| `echo -n "letmein" \| md5sum \| awk '{print $1}' > hash.txt`              | _(creates `hash.txt`)_                    |
| `john --format=raw-md5 --wordlist=/usr/share/wordlists/john.lst hash.txt` | `letmein` cracked almost instantly        |
| `john --show --format=raw-md5 hash.txt`                                   | `?:letmein` and `1 password hash cracked` |

---

## 11. CTF workflow & flag-hunting one-liners

| Command                                             | Expected output                                           |
| --------------------------------------------------- | --------------------------------------------------------- |
| `grep -ri "flag{" .`                                | any flag sitting in plain text in the current folder tree |
| `strings -n 6 file \| grep -i flag`                 | flags hidden inside a binary/image                        |
| `cat file \| base64 -d \| grep flag`                | a flag that was Base64-encoded                            |
| `exiftool * \| grep -i flag`                        | a flag tucked into a file's metadata                      |
| `binwalk -e file && grep -ri flag _file.extracted/` | a flag inside an embedded/zipped file                     |

---

## Validate every command

```bash
python3 -m pytest -v                   # run all command checks
python3 -m pytest -m "not network" -v  # offline subset
```

See [tests/test_commands.py](tests/test_commands.py). Back to the
[course plan](COURSE_PLAN.md) · [README](README.md).
