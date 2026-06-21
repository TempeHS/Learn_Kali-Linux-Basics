# Bonus Lesson — Python for Security

Security professionals **automate** boring tasks with code. Kali already has
Python 3 installed, plus the `requests` and `rich` libraries from this repo's
`requirements.txt`. In this lab you'll write a few tiny, useful tools — and then
learn how to build the same toolkit on **any** laptop, even one without Kali.

## Run Python

```bash
python3 --version
```

## Tool 1 — A simple port checker

Create a file called `portcheck.py` (use the VS Code editor) with this code:

```python
import socket

target = "scanme.nmap.org"
ports = [22, 25, 80, 443, 3389]

print(f"Checking {target} ...")
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((target, port))
    state = "OPEN" if result == 0 else "closed"
    print(f"  Port {port}: {state}")
    sock.close()
```

Run it:

```bash
python3 portcheck.py
```

You just rebuilt a mini version of Nmap! Compare your results to
[Lesson 09](09-network-scanning-nmap.md).

## Tool 2 — Inspect a website's headers

Create `headers.py`:

```python
import requests

url = "http://testphp.vulnweb.com"
response = requests.get(url, timeout=5)

print(f"Status code: {response.status_code}")
print("Server says:")
for name in ["Server", "X-Powered-By", "Content-Type"]:
    print(f"  {name}: {response.headers.get(name, 'not set')}")
```

Run it:

```bash
python3 headers.py
```

## Tool 2b — A curl-style request tool (GET, POST & endpoint probing)

This rebuilds the `curl` GET/POST workflow from [Lesson 05](05-web-recon.md) in
Python. The `requests` library does everything `curl` does — send query data,
post form or JSON bodies, and read status codes. Create `httptool.py`:

```python
import requests

# --- GET with query parameters (like: curl -G --data-urlencode) ---
resp = requests.get(
    "http://testphp.vulnweb.com/listproducts.php",
    params={"cat": 1},
    timeout=5,
)
print("GET", resp.url, "->", resp.status_code)
print(resp.text[:200])

# --- Probe several endpoints and print status codes (like a curl loop) ---
base = "http://testphp.vulnweb.com"
for path in ["/", "/robots.txt", "/admin", "/login.php", "/doesnotexist"]:
    code = requests.get(base + path, timeout=5).status_code
    print(f"  {path:<15} {code}")

# --- POST form data (like: curl -d "key=value") ---
form = requests.post(
    "https://httpbin.org/post",
    data={"username": "student", "role": "learner"},
    timeout=5,
)
print("POST form ->", form.json()["form"])

# --- POST JSON data (like: curl -H 'Content-Type: application/json' -d '{...}') ---
js = requests.post(
    "https://httpbin.org/post",
    json={"cat": 1, "note": "training"},
    timeout=5,
)
print("POST json ->", js.json()["json"])
```

Run it:

```bash
python3 httptool.py
```

> `requests` auto-sets `Content-Type: application/json` when you use `json=`,
> and URL-encodes anything in `params=` — so you rarely need to escape data by
> hand the way you do with `curl`.

## Make it pretty with rich (optional)

```python
from rich import print
print("[bold green]Scan complete![/bold green] :rocket:")
```

## Your CTF toolkit on any laptop (no Kali required)

Kali bundles hundreds of tools, but you **don't need Kali** to do most CTF work.
Python runs on Windows, macOS and Linux, and almost every Kali tool has a
pip-installable Python equivalent. That means you can practise on your own
laptop, your school computer, or a Codespace — anywhere Python is installed.

### Step 1 — Make a virtual environment (recommended)

A "venv" keeps your project's packages separate from the rest of your system.

```bash
python3 -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### Step 2 — Install the toolkit

```bash
pip install requests beautifulsoup4 dnspython python-whois \
    pycryptodome cryptography pillow exifread \
    scapy capstone pwntools python-nmap rich
```

> 💡 On Windows, `pwntools` and `scapy` work best inside **WSL** (Windows
> Subsystem for Linux). Everything else installs cleanly on plain Windows.

### What each tool replaces

These Python libraries cover the same jobs as the Kali command-line tools you
used earlier in the course:

| CTF category   | Kali tool (this course) | Python library you can pip install        | What it does                          |
| -------------- | ----------------------- | ----------------------------------------- | ------------------------------------- |
| Web recon      | `curl`, `whatweb`       | `requests`, `beautifulsoup4`              | Fetch pages, read headers, parse HTML |
| OSINT / DNS    | `dig`, `whois`          | `dnspython`, `python-whois`               | Look up DNS records and domain owners |
| Cryptography   | `openssl`               | `cryptography`, `pycryptodome`            | Hashing, AES/RSA, encryption          |
| Encoding       | `base64`, `xxd`         | `base64`, `binascii`, `codecs` (built-in) | Encode/decode data formats            |
| Steganography  | `exiftool`, `steghide`  | `pillow`, `exifread`                      | Read image metadata and pixels        |
| Forensics      | `binwalk`, `strings`    | `pillow`, built-in `re`                   | Carve and inspect file contents       |
| Network / pcap | `tshark`, `tcpdump`     | `scapy`                                   | Build, sniff and read packets         |
| Reverse eng.   | `objdump`, `radare2`    | `capstone`, `pwntools`                    | Disassemble and analyse binaries      |
| Port scanning  | `nmap`                  | `python-nmap`, `socket` (built-in)        | Scan hosts and ports                  |
| Exploitation   | —                       | `pwntools`                                | The classic CTF automation toolkit    |

### Tool 3 — Encoding & hashing with the standard library

You don't even need pip for this one — `base64`, `binascii` and `hashlib` ship
with Python. Create `encode.py`:

```python
import base64, binascii, hashlib

secret = "flag{hello}"

print("base64:", base64.b64encode(secret.encode()).decode())
print("hex:   ", binascii.hexlify(secret.encode()).decode())
print("md5:   ", hashlib.md5(secret.encode()).hexdigest())
print("sha256:", hashlib.sha256(secret.encode()).hexdigest())
```

Run it:

```bash
python3 encode.py
```

Expected output:

```text
base64: ZmxhZ3toZWxsb30=
hex:    666c61677b68656c6c6f7d
md5:    343f48218fe8b6f795a310c30c45a7ef
sha256: 959d7070b528ebcff7648617d098119a86706b0fc269d494a4e6558aaa2c8c27
```

This is CyberChef and `openssl`, rebuilt in five lines — and it runs on **any**
operating system.

### Tool 4 — Read image metadata with Pillow

This replaces `exiftool` for the basics. After `pip install pillow`, create
`exif.py`:

```python
from PIL import Image
from PIL.ExifTags import TAGS

img = Image.open("photo.jpg")          # use any JPEG you have
exif = img.getexif()

if not exif:
    print("No EXIF metadata found.")
for tag_id, value in exif.items():
    tag = TAGS.get(tag_id, tag_id)
    print(f"{tag}: {value}")
```

Hidden GPS coordinates, camera models and comments often hold the flag!

### Tool 5 — DNS lookups with dnspython

This replaces `dig`. After `pip install dnspython`, create `dns.py`:

```python
import dns.resolver

for record_type in ["A", "MX", "TXT"]:
    print(f"== {record_type} records ==")
    try:
        for answer in dns.resolver.resolve("example.com", record_type):
            print(" ", answer.to_text())
    except Exception as exc:
        print("  (none)", exc)
```

`TXT` records in particular are a favourite hiding spot for CTF flags.

### Tool 6 — Read a packet capture with Scapy

This replaces `tshark`/`tcpdump` for offline analysis. You can read a `.pcap`
file **without** admin rights (you only need root to _sniff_ live traffic):

```python
from scapy.all import rdpcap

packets = rdpcap("capture.pcap")       # a pcap from a forensics challenge
print(f"{len(packets)} packets")
for pkt in packets[:5]:
    print(pkt.summary())
```

> Want to read the raw bytes for hidden data? `bytes(pkt)` gives you every byte
> of a packet — perfect for finding flags stuffed into payloads.

## ✅ Challenge

1. Add port `21` and `8080` to `portcheck.py` and re-run it.
2. Change `headers.py` to also print the `Date` header.
3. Bonus: make `portcheck.py` ask the user for the target with
   `target = input("Target: ")`.
4. Toolkit: install the packages above in a venv and edit `encode.py` to also
   print the **base32** encoding (hint: `base64.b32encode`).
5. Toolkit: run `dns.py` against a domain of your choice and read its `TXT`
   records — what do you find?
6. Extend `httptool.py`: add a POST request that sends both a custom header
   (e.g. `User-Agent: ctf-bot`) and form data, then print the `headers` section
   of the `httpbin.org` response to confirm your header arrived.

## You finished the basics! 🎉

Next steps to keep learning safely:

- [TryHackMe](https://tryhackme.com/) — guided beginner rooms.
- [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) — Linux skills.
- [picoCTF](https://picoctf.org/) — beginner capture-the-flag challenges.

⬅️ Back to the [README](../README.md)
