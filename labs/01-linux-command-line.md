# Lesson 01 — The Linux Command Line

Kali Linux is driven from the **terminal**. Get comfortable here and everything
else becomes easy. Open a terminal in VS Code: **Terminal > New Terminal**.

## Where am I? Who am I?

```bash
whoami      # your username (should be: student)
pwd         # "print working directory" — where you are
hostname    # the name of this machine
```

## Moving around

```bash
ls          # list files here
ls -l       # long list (permissions, size, date)
ls -la      # also show hidden files (those starting with .)
cd /etc     # change directory to /etc
cd ~        # go to your home folder
cd ..       # go up one level
```

## Looking at files

```bash
cat /etc/os-release      # show a whole file
less /etc/services       # scroll a long file (press q to quit)
head -n 5 /etc/passwd    # first 5 lines
tail -n 5 /etc/passwd    # last 5 lines
```

## Making and removing things

```bash
mkdir my_first_lab       # make a folder
cd my_first_lab
echo "hello kali" > notes.txt   # create a file with text
cat notes.txt
rm notes.txt             # delete the file
cd ..
rmdir my_first_lab       # remove the empty folder
```

## Getting help

Every real tool ships with a manual. This is the most important skill of all:

```bash
man ls       # read the manual (press q to quit)
ls --help    # quick help summary
```

## Superpowers with sudo

Some actions need administrator rights. On Kali you "borrow" them with `sudo`:

```bash
sudo apt-get update      # refresh the list of installable software
```

## Searching and chaining commands

```bash
grep "root" /etc/passwd          # find lines containing "root"
cat /etc/passwd | grep "bash"    # send (pipe) output into grep
history                          # see commands you've run
```

## ✅ Challenge

1. **Do:** Create a folder called `recon`, move into it, and create `targets.txt`
   containing `scanme.nmap.org`.
2. **Verify:** Display `targets.txt` and confirm you are still in the `recon` folder.
3. **Explain:** Use `man whoami` and write one sentence describing what it does.
4. **Practice:** Return to your home directory and list files with `ls -la`.

➡️ Next: [Lesson 02 — Encoding, Decoding & CyberChef](02-cyberchef.md)
