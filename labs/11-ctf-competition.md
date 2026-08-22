# Lesson 11 — CTF Workflow Playbook & Competition 🏁

This is what everything has been building towards. A **Capture The Flag (CTF)**
is a competition where you solve security puzzles to uncover hidden **flags** —
short strings in the form `pecan{...}`. You now have a tool and a method for
every category. Time to play.

## CTF explained at high-school level

Think of a CTF like a school scavenger hunt mixed with logic puzzles:

- A teacher gives clues (the challenge).
- You investigate with tools (Linux commands, CyberChef, browser tools).
- You find the secret code (`pecan{...}`) and submit it.
- You get points and move up the leaderboard.

You are **not** breaking random real websites. You are solving legal practice
puzzles designed for learning.

> [!IMPORTANT]
> Only attack the official practice challenges and your own machines.
> See [Lesson 00](00-ethics-and-safety.md).

**Play here ➜ https://practice.pecanplus.org/?page=challenges**

## How a CTF works

1. Each challenge gives you a file, a link or a clue.
2. You find the hidden flag, e.g. `pecan{y0u_f0und_me}`.
3. You submit the flag for points. Harder challenges = more points.
4. Difficulty is shown with locks: 🔓 Beginner · 🔓🔓 Intermediate · 🔓🔓🔓 Advanced.

### What a competition round feels like

1. Start with easy flags to build confidence and points.
2. Save hard ones for later instead of getting stuck early.
3. Share notes with teammates so no work is wasted.
4. Submit often; small points add up quickly.

## Workflow playbook (how to score faster)

This section is about **process**, not just tools. Strong teams usually beat
strong individuals because they follow a repeatable workflow.

### 1. Triage first, solve second

- Read all challenge titles first.
- Start with quick-win beginner challenges in categories you already know.
- Skip hard blockers after 10-15 minutes and come back later.

### 2. Keep evidence while solving

Write commands and outputs as you go, not after you finish. This avoids losing
time re-solving a challenge from memory.

### 3. Use a consistent attempt loop

1. Identify category and likely technique.
2. Run 1-2 fast checks (metadata, strings, source view, Base64 decode).
3. If no progress, switch tools once.
4. If still blocked, park it and move to another challenge.

### 4. Team handoff format

When handing off, include:

- What you already tried.
- Exact command(s) run.
- Exact output or error.
- Current best hypothesis.

### 5. Time-box strategy

- First 30 minutes: bank easy flags quickly.
- Middle phase: medium difficulty with team collaboration.
- Final phase: revisit parked challenges with fresh context.

### 6. Remember: research is the key skill 🔎

The most-used skill in a CTF is not a Kali tool — it is **knowing how to look
things up**. Every category benefits from it: an unfamiliar file header, an
error message, a cipher name, a photo with no metadata. Before you park a
challenge, run it through the research loop from [Lesson 04](04-osint-wayback.md):

- Search the **exact string** in quotes (error, filename, odd word).
- Add `site:`, `filetype:` or `-word` to cut the noise.
- Use **Wikipedia** for the infobox, references and _View history_.
- **Reverse image search** any photo in Google Lens, TinEye _and_ Yandex.
- Run foreign text or signs through **Google Translate** (Image tab reads a
  photo), then search the local-language name.
- Confirm places on **Google Street View**, **Google Earth** (historical imagery
  and 3D terrain) and **OpenStreetMap**.
- Check the **Wayback Machine** for anything that has since been deleted.

Full walkthrough: [Lesson 04 — Search like a researcher](04-osint-wayback.md#part-d--search-like-a-researcher-).

## Pick your tool by category

| Category            | First things to try                                                                                        | Lesson                                           |
| ------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Cryptography        | CyberChef _Magic_, `base64 -d`, ROT13 brute force                                                          | [02](02-cyberchef.md) · [03](03-cryptography.md) |
| OSINT               | search operators, reverse image search, Google Translate, Street View / Earth, `exiftool`, Wayback Machine | [04](04-osint-wayback.md)                        |
| Web exploits        | view source, `robots.txt`, `gobuster`                                                                      | [05](05-web-recon.md)                            |
| Steganography       | `exiftool`, `strings`, `steghide`, `binwalk`                                                               | [06](06-steganography.md)                        |
| Forensics           | `file`, `xxd`, `binwalk -e`, `tshark`                                                                      | [07](07-forensics.md)                            |
| Reverse Engineering | `strings`, `file`, `radare2`                                                                               | [08](08-reverse-engineering.md)                  |

## A flag-hunting checklist

When you're stuck, work through these quick wins:

```bash
# Is the flag just sitting there?
grep -ri "pecan{" .

# Hidden in a binary or image?
strings -n 6 file | grep -i pecan

# If strings shows Base64-looking text, decode it
echo "cGVjYW57aGVsbG99" | base64 -d

# Encoded? Try Base64.
cat file | base64 -d 2>/dev/null | grep -i pecan

# Hidden in metadata?
exiftool file | grep -i pecan

# A file inside a file?
binwalk -e file && grep -ri pecan _file.extracted/
```

## The flag format is a key 🔑

Every PECAN+ flag looks like `pecan{...}`. That means you **already know the
first six characters of the answer before you start**. Cryptographers call this
_known plaintext_ or a _crib_, and it is the single most useful shortcut in a CTF.

Three ways to use it: **search** for it, **derive the key** from it, and
**validate** a guess with it.

### 1. Search for the format, not just the word

The flag rarely sits in plain text — but its encoded forms are just as
predictable, because encoding `pecan{` always produces the same bytes.

| Form       | What to search for                            |
| ---------- | --------------------------------------------- |
| Plain text | `pecan{`                                      |
| Hex        | `706563616e7b`                                |
| Base64     | `cGVjYW57`, `ZWNh`, `Y2Fu` (three alignments) |
| ROT13      | `crpna{`                                      |
| Reversed   | `}nacep`                                      |

```bash
# One regex that catches a whole flag, any case, printable body only
grep -rEio "pecan\{[ -~]{1,64}\}" .

# Catch the encoded forms too
grep -rEio "pecan\{|706563616e7b|cGVjYW57|crpna\{|\}nacep" .

# Base64 is chopped into 3-byte groups, so "pecan{" lands in 3 different
# alignments depending on how many bytes come before it. Search all three.
grep -rE "cGVjYW57|ZWNh|Y2Fu" .
```

> [!TIP]
> `ZWNh` and `Y2Fu` are only four characters, so they will produce false
> positives. Treat them as leads to decode, not as answers.

### 2. Derive the key from the crib

If you know the first six plaintext bytes, you can work **backwards** to the key.

```python
# xor_crib.py — recover a repeating XOR key from the known flag prefix
ciphertext = bytes.fromhex("1b040f08051a1459193e5d1a34135f1f58131f58090d5f14")
crib = b"pecan{"

key = bytes(c ^ p for c, p in zip(ciphertext, crib))
print("key bytes:", key)
```

Expected output:

```
key bytes: b'kalika'
```

That is `kali` starting to repeat, so the key is **`kali`**. Now XOR it back over
the whole ciphertext to reveal the rest of the flag:

```python
key = b"kali"
flag = bytes(c ^ key[i % len(key)] for i, c in enumerate(ciphertext))
print(flag.decode())
```

Expected output:

```
pecan{x0r_1s_r3v3rs1bl3}
```

The same idea works for a Caesar/ROT shift: find the shift that turns the first
letter into `p`, and you have solved the entire message in one step.

### 3. Force `peca`, then test the 5th character

When brute forcing, don't eyeball 256 lines of garbage. Make the computer check
the format for you. Match a **short prefix** so near-misses still surface, then
**confirm** with the next character.

Make a practice file to try it on:

```bash
echo "322721232c3931732c252e711d203b36711d3a72303f" | xxd -r -p > challenge.bin
```

```python
# brute_xor.py — try every single-byte XOR key and filter by the flag format
data = open("challenge.bin", "rb").read()

for key in range(256):
    out = bytes(b ^ key for b in data)
    hit = out.lower().find(b"peca")        # force the first four characters
    if hit == -1:
        continue
    if out[hit + 4:hit + 5].lower() != b"n":   # 5th character must be 'n'
        continue                                # otherwise it's a coincidence
    print(f"key={key:#04x} -> {out[hit:hit + 64]}")
```

Expected output:

```
key=0x42 -> b'pecan{s1ngl3_byt3_x0r}'
key=0x62 -> b'PECAN[S\x11NGL\x13\x7fBYT\x13\x7fX\x10R]'
```

Two hits, because the search is case-insensitive. Rule 4 below settles it: only
the first has a real `{` and a clean lowercase body, so `0x42` is the key.

Why two stages? `peca` alone appears by chance often enough to be noisy, and
demanding the full `pecan{` immediately can miss a flag whose brace was mangled
by an off-by-one or a bad decode. Prefix-then-verify catches partial successes
that a strict search throws away.

The same filter works in a shell brute force:

```bash
# Try all 25 ROT shifts and keep only lines that look like a flag
CIPHER="wljhu{y0a_1z_3hzf}"

for k in $(seq 1 25); do
  echo "$CIPHER" | tr "a-z" "$(echo {a..z} | tr -d ' ' | sed "s/^\(.\{$k\}\)\(.*\)/\2\1/")"
done | grep -Ei "peca"
```

Expected output:

```
pecan{r0t_1s_3asy}
```

### 4. Validate a decode with the format's rules

Use these to decide whether a half-readable decode is on the right track:

- The body is almost always lowercase `a-z`, digits and underscores.
- There is exactly one `{` and one closing `}`.
- Flags are typically 10-60 characters — a 5,000-character "flag" is wrong.
- If `pecan` decodes cleanly but the body is gibberish, you have the right
  cipher and the **wrong key length**.

> [!IMPORTANT]
> Submit the flag **exactly** as found, braces included. Don't retype it — copy
> it, or you will lose points to a typo.

## Secret-leak triage (Git and env files)

Many miscellaneous web CTF tasks hide flags in source history or config mistakes.
Always check these early when a challenge gives you source code or a repo.

Quick reference: [Git and env secret leak checks](../CHEATSHEET.md#git-and-env-secret-leak-checks).

```bash
# Current tree: look for obvious secret-like files
find . -maxdepth 3 -type f \( -name "*.env" -o -name "*.bak" -o -name "*config*" \)

# Search tracked files for common secret patterns
grep -RInE "pecan\{|flag\{|API_KEY|SECRET|TOKEN|PASSWORD" .

# If this is a git repo, inspect recent commits and changed files
git log --oneline -n 10
git show --name-only --oneline HEAD
```

If the challenge is clearly git-history based, check earlier commits too:

```bash
git log --all --name-only --pretty=format:"commit %h %s" | head -n 80
```

Expected clues:

- Secrets removed in a newer commit but present in older history.
- `.env` or backup files accidentally committed.
- Hard-coded tokens/flags in source comments or test data.

## Suggested first solves (all Beginner 🔓)

Work these in order — each maps directly to a lesson you've finished:

1. **Cryptography → _Encoded_** — decode with CyberChef.
2. **Steganography → _Head in the clouds_** — `exiftool` / `strings`.
3. **Web exploits → _Bite my shiny metal_** — check `robots.txt`.
4. **OSINT → _Kidnapped part 1_** — search operators, reverse image search + Wayback.
5. **Forensics → _3D flag_** — identify and open the file.
6. **Reverse Engineering → _Love letter_** — `strings` the binary.

## ✅ Challenge

1. **Do:** Choose three beginner challenges from different categories and solve them.
2. **Verify:** Record the exact commands you used and one key clue for each solve.
3. **Explain:** Write a one-sentence handoff note for one unsolved challenge.
4. **Practice:** Submit your solved flags and summarize which technique worked best.

## Keep a write-up

For every flag you capture, note:

- The challenge name and category.
- The commands that worked.
- The flag.

Write-ups are the single best way to revise — and they look great in a portfolio.

Suggested template for each solve:

- Challenge name/category.
- Initial clue and hypothesis.
- Commands tried.
- Final flag and why it worked.
- Any dead ends (what did not work) so teammates avoid repeating them.

## Compete for real

When you're landing Beginner and Intermediate flags, enter the live competition:

- **Register:** [pecanplus.org/register.html](https://pecanplus.org/register.html)
- **Choose a division:** [Division Decision Guide](https://pecanplus.org/assets/DivisionDecisionGuide.pdf)

## Keep levelling up

- [picoCTF](https://picoctf.org/) · [TryHackMe](https://tryhackme.com/) ·
  [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)
- Bonus skills: [Python for Security](12-python-scripting.md) to automate your solves.

🎉 **You've completed the course. Go capture some flags!**

⬅️ Back to the [Course Plan](../COURSE_PLAN.md) · [README](../README.md)
