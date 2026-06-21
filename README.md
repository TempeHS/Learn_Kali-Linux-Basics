# Learn Kali Linux Basics

A ready-to-go **Kali Linux** lab in a Dev Container for high school students to
learn **basic Cyber Security skills** safely. Open it in GitHub Codespaces or
VS Code and you get a real Kali terminal with a curated set of beginner tools —
no messy install, no risk to your own computer.

> [!IMPORTANT]
> Only use these tools on systems you **own** or have **written permission** to
> test, plus the built-in DVWA container and the public practice targets listed
> in the labs. Attacking systems without permission is illegal.
> See [Lab 00](labs/00-ethics-and-safety.md).

## Description

This repository is a self-contained Kali Linux learning environment for
introductory cyber security and CTF practice. When the container builds you get
the official `kalilinux/kali-rolling` image plus the tools needed for the
curriculum: the Linux command line, network discovery, web reconnaissance,
password basics and a little Python scripting.

It also ships a **built-in practice website**: a
[DVWA (Damn Vulnerable Web Application)](https://github.com/digininja/DVWA)
container starts automatically alongside Kali, so the web-recon and exploitation
labs work **offline** with no external target. From the Kali terminal it is
reachable at **`http://dvwa`**, and in a browser tab at
**`http://localhost:4280`** (log in with **`admin` / `password`**, then set the
DVWA Security level to **Low**).

Everything runs inside a **disposable container** as a normal `student` user, so
you can experiment freely and just rebuild if anything breaks.

## Getting Started

### Dependencies

- A GitHub account (for Codespaces), **or**
- [VS Code](https://code.visualstudio.com/) +
  [Docker Desktop](https://www.docker.com/products/docker-desktop/) +
  the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  extension.

### Installing

**Option A — GitHub Codespaces (easiest):**

1. Click the green **`< > Code`** button on this repo.
2. Choose the **Codespaces** tab and **Create codespace on main**.
3. Wait a few minutes for Kali to build. Done!

**Option B — Locally with VS Code:**

1. Clone the repo:
   ```bash
   git clone https://github.com/TempeHS/Learn_Kali-Linux-Basics.git
   ```
2. Open the folder in VS Code.
3. When prompted, click **Reopen in Container** (or run
   _Dev Containers: Reopen in Container_ from the Command Palette).

### Executing program

Open a terminal in VS Code (**Terminal > New Terminal**) and try:

```bash
# Confirm you are the student user on Kali
whoami && cat /etc/os-release | head -n 1

# Check a tool is installed
nmap --version
```

Then work through the lessons in order, starting with
[labs/00-ethics-and-safety.md](labs/00-ethics-and-safety.md).

## Lessons

| #   | Lesson                                                                             | Skill                          |
| --- | ---------------------------------------------------------------------------------- | ------------------------------ |
| 00  | [Ethics & Safety](labs/00-ethics-and-safety.md)                                    | Stay legal and responsible     |
| 01  | [Linux Command Line](labs/01-linux-command-line.md)                                | Navigate and use the shell     |
| 02  | [Encoding, Decoding & CyberChef](labs/02-cyberchef.md)                             | Decode data with CyberChef     |
| 03  | [Cryptography Basics](labs/03-cryptography.md)                                     | Caesar, XOR, hashes, AES       |
| 04  | [OSINT & the Wayback Machine](labs/04-osint-wayback.md)                            | Find public info & old sites   |
| 05  | [Web Reconnaissance & Exploitation Basics](labs/05-web-recon.md)                   | Web recon plus input testing   |
| 06  | [Steganography](labs/06-steganography.md)                                          | Find data hidden in files      |
| 07  | [Forensics](labs/07-forensics.md)                                                  | File carving & packet captures |
| 08  | [Reverse Engineering & Binary Exploitation Basics](labs/08-reverse-engineering.md) | RE plus pwn foundations        |
| 09  | [Network Scanning with Nmap](labs/09-network-scanning-nmap.md)                     | Discover hosts & ports         |
| 10  | [Password & Hash Basics](labs/10-passwords-and-hashes.md)                          | Understand password security   |
| 11  | [CTF Workflow Playbook & Competition](labs/11-ctf-competition.md)                  | Triage, teamwork, score points |
| ★   | [Python for Security](labs/12-python-scripting.md)                                 | Bonus: automate your solves    |

## CTF Course

Working towards a competition? Follow the full
[Kali Linux & CTF course plan](COURSE_PLAN.md) — 12 lessons (including
**CyberChef** and the **Wayback Machine**) that prepare you for the
[PECAN+ practice CTF](https://practice.pecanplus.org/). Every command in the
course is checked by an automated test suite:

```bash
python3 -m pytest -v                     # validate all commands in this codespace
python3 -m pytest -m "not network" -v    # offline subset
```

Keep the [Kali Linux & CTF Cheat Sheet](CHEATSHEET.md) handy — every command
with its expected output, grouped by CTF category.

## Included Tools

Networking: `nmap`, `whois`, `dnsutils`, `traceroute`, `tcpdump`, `tshark`,
`netcat`, `net-tools` ·
Web: `nikto`, `dirb`, `gobuster`, `whatweb`, `sqlmap` ·
Passwords: `john`, `hydra`, `hashid` ·
Scripting: `python3`, `pip`, `git`.

## Help

- **Container won't build?** Open the Command Palette and run
  _Dev Containers: Rebuild Container_.
- **A command says "permission denied"?** Prefix it with `sudo`.
- **Want a tool that isn't installed?** Add it in
  [.devcontainer/Dockerfile](.devcontainer/Dockerfile) and rebuild, e.g.
  `sudo apt-get update && sudo apt-get install <package>`.

### DVWA practice site (Lessons 05 & 09)

Need setup, login, troubleshooting, or cookie help for DVWA?

- Use the dedicated guide: [DVWA Help Guide](DVWA_HELP.md)
- Lessons that use it: [Lesson 05](labs/05-web-recon.md),
  [Lesson 09](labs/09-network-scanning-nmap.md)

```bash
man nmap   # every tool has a manual — read it!
```

## Authors

- [@benpaddlejones](https://github.com/benpaddlejones)

## Version History

- 2.0
  - Added a built-in DVWA practice site so the web-recon and exploitation labs
    run offline, with matching lab updates and database-readiness tests.
- 1.0
  - Released as a Kali Linux cyber security lab with beginner-friendly lessons,
    tests, and CTF-aligned content.
- 0.1
  - Initial Release

## License

This project is licensed under the GNU General Public License v3.0 - see the
[LICENSE](LICENSE) file for details.

## Acknowledgments

- [Kali Linux](https://www.kali.org/)
- [Kali Tools documentation](https://www.kali.org/tools/)
- [Nmap public test server: scanme.nmap.org](http://scanme.nmap.org/)
- [DVWA (Damn Vulnerable Web Application)](https://github.com/digininja/DVWA)
- [DVWA Docker image](https://github.com/digininja/DVWA/pkgs/container/dvwa)
