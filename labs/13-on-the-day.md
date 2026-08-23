# Lab 13 - On the Day Checklist

Use this checklist before competition day so your team can start on time and
stay in contact.

## Confirm your entry

- [ ] Register at [pecanplus.org/register.html](https://pecanplus.org/register.html).
- [ ] Use the [Division Decision Guide](https://pecanplus.org/assets/DivisionDecisionGuide.pdf)
      to confirm your division.
- [ ] Check the event date, arrival time, location and competition rules.
- [ ] Make sure every teammate knows the plan.

## What to bring

- [ ] A laptop with a working **Kali Linux VirtualBox VM**
- [ ] Laptop charger
- [ ] Notebook
- [ ] Pens
- [ ] Snacks
- [ ] Water bottle
- [ ] Access to your team's Discord server

## Set up Kali Linux in VirtualBox

Complete this setup before competition day.

1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
2. Download the official **VirtualBox** image from
   [Kali Linux Pre-Built Virtual Machines](https://www.kali.org/get-kali/#kali-virtual-machines).
3. Verify the downloaded image's checksum by following Kali's
   [download verification guide](https://www.kali.org/docs/introduction/download-official-kali-linux-images/).
4. Extract the downloaded archive.
5. Open VirtualBox and choose **Add**, then select the extracted `.vbox` file.
6. Start the VM and sign in. The default credentials for the official pre-built
   image are `kali` / `kali`; change the password after your first login.
7. Open a terminal and update Kali:

   ```bash
   sudo apt update
   sudo apt full-upgrade -y
   ```

8. Install the tools used throughout this course:

   ```bash
   sudo apt install -y \
     curl wget unzip python3 python3-pip python3-venv python3-requests python3-rich \
     net-tools iputils-ping iproute2 dnsutils whois traceroute netcat-traditional tcpdump \
     nmap nikto dirb gobuster sqlmap whatweb john hydra hashid tshark \
     openssl xxd file binutils binwalk foremost libimage-exiftool-perl \
     steghide imagemagick pngcheck gdb radare2
   ```

   These packages cover the command line, networking, web reconnaissance,
   passwords and hashes, packet analysis, cryptography, steganography,
   forensics, reverse engineering, and Python labs. CyberChef and the Wayback
   Machine run in a web browser and do not need to be installed.

9. Restart the VM and confirm it can access the internet.

> [!IMPORTANT]
> Download and update the VM at home. Competition Wi-Fi may be slow or may not
> allow large downloads.

## Test your VM before leaving home

Open a terminal in Kali and run:

```bash
whoami
cat /etc/os-release | head -n 1
ip address
for tool in nmap gobuster john tshark exiftool steghide binwalk radare2; do
   command -v "$tool" || echo "MISSING: $tool"
done
```

Confirm that:

- Kali starts without errors.
- You know your VM username and password.
- The keyboard, mouse, internet connection, and clipboard work.
- The tool check does not print any `MISSING` messages.
- Your laptop charger works and the battery is charged.
- You have enough free disk space for challenge files.

## Using AI during the competition

Always read and follow the competition's official rules. They take priority
over this guide. If you are unsure whether a use of AI is permitted, ask an
organiser before using it.

AI may generally be used as a **tool in targeted ways**, such as:

- Explaining a command, error message, file format, or security concept.
- Suggesting a tool or technique to investigate a specific clue.
- Helping correct the syntax of a command or a small script you wrote.
- Giving a hint while you and your team perform the actual investigation.

> [!WARNING]
> Do not use generative AI to solve an entire challenge for you. Pasting a
> complete problem into an AI service and submitting its answer as your own is
> not allowed. Teams may be disqualified for relying heavily on AI or for
> submitting solves that were not achieved in the spirit of ethical,
> human-driven participation.

You and your team must understand, test, and verify any AI-assisted work. Do
not share flags, credentials, personal information, or competition-only files
with a public AI service.

## Set up team communication

Create or join a **Discord server for your team** before the event.

- Make sure every teammate has joined.
- Create a channel for arrival updates and announcements.
- Create a channel for sharing challenge notes and progress.
- Turn on notifications for the arrival channel.
- Post there if you are running late or your plans change.
- Never post passwords, flags, or sensitive personal information in a public
  channel.

## Final check

Before you leave, check that you have your laptop and charger, Kali VM,
notebook, pens, snacks, water bottle, and Discord access.

Back to the [README](../README.md)
