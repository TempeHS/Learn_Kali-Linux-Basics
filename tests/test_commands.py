"""Validate that every command taught in the course works in this codespace.

Run all checks:           python3 -m pytest -v
Skip internet checks:     python3 -m pytest -m "not network" -v

Each test runs a real command with subprocess and asserts on its output, so a
green run proves the lessons in COURSE_PLAN.md and labs/ are reproducible here.
"""

import hashlib
import shutil
import socket
import subprocess
import urllib.request

import pytest


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def run(cmd, **kwargs):
    """Run a shell command and return the CompletedProcess (text mode)."""
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=kwargs.pop("timeout", 60),
        **kwargs,
    )


def have_internet(host="archive.org", port=443, timeout=5):
    try:
        socket.create_connection((host, port), timeout=timeout).close()
        return True
    except OSError:
        return False


requires_net = pytest.mark.skipif(
    not have_internet(), reason="no internet connectivity available"
)


# DVWA runs as a local sidecar container (see .devcontainer/docker-compose.yml)
# and is reachable from the workspace at http://dvwa. It replaces the external
# testphp.vulnweb.com demo site for web-recon practice so the tests work offline.
DVWA_HOST = "dvwa"
DVWA_URL = f"http://{DVWA_HOST}"


def dvwa_reachable(host=DVWA_HOST, port=80, timeout=5):
    try:
        socket.create_connection((host, port), timeout=timeout).close()
        return True
    except OSError:
        return False


def dvwa_db_ready(timeout=10):
    """True only when DVWA's database backend is connected.

    DVWA's web server answers on port 80 even when its database is down, but the
    login page then renders a PHP/MySQL "Fatal error" instead of the real form.
    A working database is proved by the page rendering its CSRF ``user_token``.
    """
    if not dvwa_reachable():
        return False
    try:
        with urllib.request.urlopen(f"{DVWA_URL}/login.php", timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace").lower()
    except OSError:
        return False
    if "fatal error" in body or "connection refused" in body or "sqlstate" in body:
        return False
    return "user_token" in body


requires_dvwa = pytest.mark.skipif(
    not dvwa_reachable(), reason="DVWA container not reachable at http://dvwa"
)

requires_dvwa_db = pytest.mark.skipif(
    not dvwa_db_ready(),
    reason=(
        "DVWA database not ready — open http://localhost:4280 and run "
        "Setup / Create / Reset Database"
    ),
)


# --------------------------------------------------------------------------- #
# Lesson 0/1 — the tools exist (every command used in the course)
# --------------------------------------------------------------------------- #
TOOLS = [
    # Core shell
    "bash", "ls", "cat", "grep", "find", "man", "tr", "whoami",
    "pwd", "hostname", "head", "tail", "mkdir", "rm", "rmdir",
    "less", "awk", "python3", "gzip", "printf", "sudo", "apt-get",
    # Encoding / crypto (Lessons 2 & 3)
    "base64", "base32", "xxd", "openssl", "md5sum", "sha256sum",
    # OSINT / network (Lessons 4 & 9)
    "curl", "whois", "dig", "nslookup", "nmap", "nc",
    # Web (Lesson 5)
    "whatweb", "gobuster", "dirb", "nikto", "sqlmap",
    # Steganography / forensics (Lessons 6 & 7)
    "file", "strings", "exiftool", "steghide", "binwalk", "foremost",
    "pngcheck", "convert", "tshark", "tcpdump",
    # Reverse engineering (Lesson 8)
    "objdump", "gdb", "radare2",
    # Passwords (Lesson 10)
    "john", "hashid",
]


@pytest.mark.parametrize("tool", TOOLS)
def test_tool_installed(tool):
    assert shutil.which(tool) is not None, f"{tool} is not installed/on PATH"


# --------------------------------------------------------------------------- #
# Lesson 2 — Encoding / decoding (CyberChef equivalents)
# --------------------------------------------------------------------------- #
def test_base64_decode():
    r = run('echo -n "cGVjYW57aGVsbG99" | base64 -d')
    assert r.stdout == "pecan{hello}"


def test_base64_encode():
    r = run('echo -n "pecan{hello}" | base64')
    assert r.stdout.strip() == "cGVjYW57aGVsbG99"


def test_hex_decode():
    r = run('echo -n "70 65 63 61 6e" | xxd -r -p')
    assert r.stdout == "pecan"


def test_hex_encode():
    r = run('echo -n "pecan" | xxd -p')
    assert r.stdout.strip() == "706563616e"


def test_rot13():
    r = run("echo \"Uryyb\" | tr 'A-Za-z' 'N-ZA-Mn-za-m'")
    assert r.stdout.strip() == "Hello"


def test_base32_encode():
    r = run('echo -n "pecan" | base32')
    assert r.stdout.strip() == "OBSWGYLO"


def test_lesson1_basic_identity_commands():
    r1 = run("whoami")
    r2 = run("pwd")
    r3 = run("hostname")
    assert r1.returncode == 0 and r1.stdout.strip() != ""
    assert r2.returncode == 0 and r2.stdout.strip().startswith("/")
    assert r3.returncode == 0 and r3.stdout.strip() != ""


def test_lesson1_file_create_and_remove(tmp_path):
    r = run(
        f"cd {tmp_path} && mkdir my_first_lab && cd my_first_lab && "
        "echo 'hello kali' > notes.txt && cat notes.txt && rm notes.txt && "
        "cd .. && rmdir my_first_lab"
    )
    assert "hello kali" in r.stdout


def test_man_page_exists_without_interactive_pager():
    # Equivalent to checking that `man ls` is available in this environment.
    r = run("man -w ls")
    assert r.returncode == 0 and r.stdout.strip() != ""


# --------------------------------------------------------------------------- #
# Lesson 3 — Cryptography / hashing
# --------------------------------------------------------------------------- #
def test_md5sum_known_value():
    r = run('echo -n "password123" | md5sum')
    assert r.stdout.strip() == "482c811da5d5b4bc6d497ffa98491e38  -"


def test_sha256sum_known_value():
    r = run('echo -n "secret" | sha256sum')
    assert r.stdout.strip() == (
        "2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b  -"
    )


def test_openssl_sha256_matches_python():
    expected = (
        "2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b"
    )
    assert expected == hashlib.sha256(b"secret").hexdigest()
    r = run('echo -n "secret" | openssl dgst -sha256')
    assert expected in r.stdout


def test_openssl_encrypt_decrypt_round_trip(tmp_path):
    msg = tmp_path / "msg.txt"
    enc = tmp_path / "msg.enc"
    msg.write_text("pecan{crypto}")
    run(
        f"openssl enc -aes-256-cbc -pbkdf2 -pass pass:mykey "
        f"-in {msg} -out {enc}"
    )
    r = run(
        f"openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:mykey -in {enc}"
    )
    assert r.stdout == "pecan{crypto}"


def test_caesar_bruteforce_python_snippet():
    r = run(
        "python3 - <<'PY'\n"
        'ct = "Khoor"\n'
        "for s in range(26):\n"
        '    out = "".join(\n'
        "        chr((ord(c) - base + s) % 26 + base) if c.isalpha() else c\n"
        "        for c in ct\n"
        "        for base in [65 if c.isupper() else 97]\n"
        "    )\n"
        '    print(f"shift {s:2}: {out}")\n'
        "PY"
    )
    assert "shift 23: Hello" in r.stdout


def test_xor_python_snippet():
    r = run("python3 -c \"print(bytes([b ^ 0x42 for b in b'\\x32\\x27\\x21\\x23\\x2c']).decode())\"")
    assert r.stdout.strip() == "pecan"


# --------------------------------------------------------------------------- #
# Lesson 6 — Steganography
# --------------------------------------------------------------------------- #
def test_exiftool_read_comment(tmp_path):
    img = tmp_path / "suspect.png"
    run(f"convert -size 64x64 xc:skyblue {img}")
    run(f'exiftool -overwrite_original -Comment="pecan{{exif_hunter}}" {img}')
    r = run(f"exiftool -Comment {img}")
    assert "pecan{exif_hunter}" in r.stdout


def test_strings_finds_flag(tmp_path):
    blob = tmp_path / "blob.png"
    run(f"printf '\\x89PNG\\x00pecan{{in_the_bytes}}\\x00' > {blob}")
    r = run(f"strings {blob} | grep pecan")
    assert "pecan{in_the_bytes}" in r.stdout


def test_steghide_embed_and_extract(tmp_path):
    cover = tmp_path / "cover.bmp"
    secret = tmp_path / "flag.txt"
    stego = tmp_path / "out.bmp"
    out = tmp_path / "revealed.txt"
    run(f"convert -size 200x200 xc:gray BMP3:{cover}")
    run(f'echo "pecan{{stego_master}}" > {secret}')
    embed = run(
        f"steghide embed -cf {cover} -ef {secret} -sf {stego} "
        f"-p hunter2 -q"
    )
    assert embed.returncode == 0, embed.stderr
    run(f"steghide extract -sf {stego} -p hunter2 -xf {out} -q")
    assert out.read_text().strip() == "pecan{stego_master}"


def test_binwalk_detects_embedded_gzip(tmp_path):
    cover = tmp_path / "cover.bmp"
    gz = tmp_path / "secret.gz"
    combo = tmp_path / "combo.bmp"
    run(f"convert -size 200x200 xc:gray BMP3:{cover}")
    run(f'echo "pecan{{hidden_zip}}" | gzip > {gz}')
    run(f"cat {cover} {gz} > {combo}")
    r = run(f"binwalk {combo}")
    assert "gzip" in r.stdout.lower()


# --------------------------------------------------------------------------- #
# Lesson 7 — Forensics
# --------------------------------------------------------------------------- #
def test_file_identifies_png(tmp_path):
    mystery = tmp_path / "mystery"
    run(f"convert -size 8x8 xc:red PNG:{mystery}")
    r = run(f"file {mystery}")
    assert "PNG image data, 8 x 8, 1-bit colormap, non-interlaced" in r.stdout


def test_xxd_png_magic(tmp_path):
    mystery = tmp_path / "mystery"
    run(f"convert -size 8x8 xc:red PNG:{mystery}")
    r = run(f"xxd {mystery} | head -2")
    assert "8950 4e47" in r.stdout


def test_pngcheck_valid_png(tmp_path):
    png = tmp_path / "pic.png"
    run(f"convert -size 8x8 xc:white {png}")
    r = run(f"pngcheck {png}")
    assert "OK" in r.stdout


# --------------------------------------------------------------------------- #
# Lesson 8 — Reverse engineering
# --------------------------------------------------------------------------- #
def test_file_identifies_elf():
    # Lesson 08: python3 resolves to a known ELF binary.
    py = shutil.which("python3")
    r = run(f"file -L {py}")
    assert "ELF 64-bit LSB" in r.stdout


def test_objdump_reads_elf():
    # python3 is a known ELF binary on Kali.
    py = shutil.which("python3")
    r = run(f"objdump -f {py} | head -4")
    assert "file format elf" in r.stdout.lower()
    assert "architecture:" in r.stdout


def test_radare2_version():
    r = run("radare2 -v | head -1")
    assert "radare2" in r.stdout.lower()


def test_gdb_info_files_command():
    r = run('gdb -q /bin/ls -ex "info files" -ex "quit" | head -n 8')
    # gdb may resolve /bin/ls to /usr/bin/ls depending on the distro layout.
    assert 'Symbols from "' in (r.stdout + r.stderr)


def test_pwn_cyclic_pattern_prefix():
    r = run(
        "python3 - <<'PY'\n"
        "import string\n"
        "alphabet = string.ascii_lowercase\n"
        "pattern = ''.join(a + b + c for a in alphabet for b in alphabet for c in alphabet)\n"
        "print(pattern[:24])\n"
        "PY"
    )
    assert r.stdout.strip() == "aaaaabaacaadaaeaafaagaah"


def test_little_endian_pack_example():
    r = run("python3 -c \"import struct; print(struct.pack('<I', 0x41424344).hex())\"")
    assert r.stdout.strip() == "44434241"


# --------------------------------------------------------------------------- #
# Lesson 10 — Passwords & hashes
# --------------------------------------------------------------------------- #
def test_hashid_identifies_md5():
    r = run("hashid 5f4dcc3b5aa765d61d8327deb882cf99")
    assert "MD5" in r.stdout


def test_john_cracks_known_md5(tmp_path):
    hash_file = tmp_path / "hash.txt"
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("letmein\n")
    hash_file.write_text("0d107d09f5bbe40cade3de5c71e9e9b7\n")  # letmein
    run(
        f"john --format=raw-md5 --wordlist={wordlist} {hash_file}",
        timeout=120,
    )
    shown = run(f"john --show --format=raw-md5 {hash_file}")
    assert "letmein" in shown.stdout.lower()


# --------------------------------------------------------------------------- #
# Lessons 4/5/9 — Internet-dependent commands (legal targets only)
# --------------------------------------------------------------------------- #
@pytest.mark.network
@requires_net
def test_wayback_machine_api():
    # Lesson 4: the Wayback Machine availability API returns archived snapshots.
    r = run(
        'curl -s "http://archive.org/wayback/available?url=example.com"'
    )
    assert "archived_snapshots" in r.stdout


@pytest.mark.network
@requires_net
def test_practice_ctf_reachable():
    # Lesson 11: the PECAN+ practice CTF is online.
    r = run(
        'curl -s -o /dev/null -w "%{http_code}" '
        "https://practice.pecanplus.org/"
    )
    assert r.stdout.strip() == "200"


@pytest.mark.network
@requires_net
def test_curl_fetches_page():
    # Lessons 4 & 5: fetching a page with curl (recon basics).
    r = run('curl -s --max-time 20 https://example.com')
    assert "Example Domain" in r.stdout


@pytest.mark.network
@requires_net
def test_whois_returns_output():
    r = run("whois example.com | head -n 5")
    assert r.returncode == 0 and r.stdout.strip() != ""


@pytest.mark.network
@requires_net
def test_nslookup_resolves_vulnweb():
    r = run("nslookup testphp.vulnweb.com")
    assert "Address" in r.stdout


@requires_dvwa
def test_whatweb_detects_target():
    r = run(f"whatweb {DVWA_URL}", timeout=120)
    assert "dvwa" in r.stdout.lower()


@requires_dvwa
def test_dvwa_database_backend_ready():
    # DVWA's web server answers even with no database, but the login page then
    # shows a PHP/MySQL "Fatal error" instead of the form. This test fails (not
    # skips) when the site is up but the database is missing, so students get a
    # clear, actionable signal to run Setup / Create / Reset Database.
    r = run(f'curl -s "{DVWA_URL}/login.php"')
    body = r.stdout.lower()
    assert "fatal error" not in body and "connection refused" not in body, (
        "DVWA is running but its database is not connected. Open "
        "http://localhost:4280 and click 'Create / Reset Database', or rebuild "
        "the dev container."
    )
    # The CSRF token only renders once the app has initialised against its DB.
    assert "user_token" in body


@requires_dvwa_db
def test_web_parameter_probe_endpoint_responds():
    # With the database connected, DVWA's login page renders its real form and
    # identifies the app, proving the vulnerable target is ready for the
    # web-recon exercises.
    r = run(f'curl -s "{DVWA_URL}/login.php"')
    body = r.stdout.lower()
    assert "dvwa" in body
    assert "username" in body and "password" in body


def test_sqlmap_version():
    r = run("sqlmap --version")
    assert r.returncode == 0 and r.stdout.strip() != ""


@pytest.mark.network
@requires_net
def test_dig_resolves():
    # Lesson 4 & 9: DNS lookup of a legal practice host.
    r = run("dig +short scanme.nmap.org")
    assert "45.33.32.156" in r.stdout


@pytest.mark.network
@requires_net
def test_nmap_scans_scanme():
    # Lesson 9: Nmap's official legal scanning target (TCP connect scan).
    r = run("nmap -sT -Pn -p 80 scanme.nmap.org", timeout=120)
    assert "scanme.nmap.org" in r.stdout
