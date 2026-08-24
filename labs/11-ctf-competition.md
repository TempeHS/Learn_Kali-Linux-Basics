# Lesson 11 — Your First CTF Competition 🏁

This is what everything has been building towards. A **Capture The Flag (CTF)**
is a competition where you solve security puzzles to uncover hidden **flags** —
short strings in the form `pecan{...}`. This lesson shows you what to do during
your first competition.

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
3. You submit the flag for points. There are no difficulty indicators, so you must actively triage to figure out what is hard and what is easy!

## Understanding Scoring and Triage

In a CTF, effective triage and understanding how scoring works are just as important as technical skills. Here is some practical advice for maximizing your team's score:

**Scoring Mechanics**

- **Dynamic Scoring:** PECAN+ uses dynamic scoring. This means every challenge starts at maximum points (e.g. 500), but as more teams solve it, its value drops for _everyone_. A challenge solved by 50 teams might end up worth only 50 points.
- **The Catch:** If you spend 3 hours solving a hard problem that no one else can solve, you keep all 500 points. But if you ignore an easy challenge, and 100 teams solve it, its value drops so low it barely matters.
- **No Difficulty Indicators:** There are no "beginner" or "advanced" labels. You must use the solve count as your only gauge of how hard a challenge is.

**Practical Triage Advice in a Dynamic Game**

- **Harvest the "easy" points fast:** If a challenge has a lot of solves, it is easy or straightforward. Solve it immediately to grab a share of those shrinking points before they hit the floor.
- **Save the hard challenges for later:** An unwieldy, 0-solve challenge will keep its maximum point value all day. You don't lose value by waiting to tackle it in the afternoon.
- **Check the solves counter constantly:** If you see a challenge suddenly jumping in solves, another team might have found the trick. Pivot and grab it!
- **Divide by category, not difficulty:** Have teammates focus on their strengths. If one person loves OSINT, let them clear out all the OSINT challenges before moving to Web.
- **Timebox yourself:** If you make zero progress or have no new ideas after 15 minutes on a challenge, park it and switch. You can always come back with a fresh perspective.

## Your first 10 minutes

1. Scan every challenge title and its current solve count before choosing one.
2. Pick a highly-solved challenge in a category you recognise.
3. Tell your team which challenge you are trying.
4. Open a notes document and record the challenge name.
5. Start with one or two quick checks instead of trying every tool.

Do not worry if another challenge looks confusing. You are not expected to
solve the challenges in order.

## Use this solve loop

Repeat these six steps for every challenge:

1. **Read:** What files, links, hints and unusual words were provided?
2. **Classify:** Is it likely cryptography, OSINT, web, steganography,
   forensics or reverse engineering?
3. **Check:** Try one or two quick techniques from the table below.
4. **Record:** Save each command and its useful output in your notes.
5. **Decide:** After 10–15 minutes without progress, ask for help or park it.
6. **Submit:** Copy the complete `pecan{...}` flag and check that it was accepted.

Parking a challenge is good time management, not giving up. Return to it after
banking easier points or when a teammate has a new idea.

## Pick a first check by category

| Category            | Start with                                       | Lesson                                           |
| ------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Cryptography        | CyberChef _Magic_, Base64 or ROT13               | [02](02-cyberchef.md) · [03](03-cryptography.md) |
| OSINT               | Search the exact clue or reverse-search an image | [04](04-osint-wayback.md)                        |
| Web exploits        | View source and check `robots.txt`               | [05](05-web-recon.md)                            |
| Steganography       | `exiftool file` and `strings file`               | [06](06-steganography.md)                        |
| Forensics           | `file`, `xxd` and `binwalk`                      | [07](07-forensics.md)                            |
| Reverse Engineering | `file` and `strings`                             | [08](08-reverse-engineering.md)                  |

## When you are stuck

Try only the checks that fit the challenge:

```bash
file challenge-file
strings challenge-file | head
exiftool challenge-file
grep -ri "pecan{" .
```

If a clue contains an unfamiliar phrase or error, search for the exact text in
quotes. For photos, deleted pages and location clues, use the full research
loop in [Lesson 04](04-osint-wayback.md). The complete command reference is in
the [CTF cheat sheet](../CHEATSHEET.md#11-ctf-workflow--flag-hunting-one-liners).

## Work as a team

### Share progress

Tell your teammates when you start, park or solve a challenge. This prevents
two people unknowingly repeating the same work.

### Use this handoff note

```text
Challenge:
What I tried:
Useful output or error:
My best guess:
```

### Change focus as time passes

- **First 30 minutes:** collect the most solved flags.
- **Middle:** collaborate on challenges where someone has found a useful clue.
- **Final phase:** revisit parked challenges and check unsubmitted flags.

## Suggested first solves (practice site only)

Work these in order — each maps directly to a lesson you've finished:

1. **Cryptography → _Encoded_** — decode with CyberChef.
2. **Steganography → _Head in the clouds_** — `exiftool` / `strings`.
3. **Web exploits → _Bite my shiny metal_** — check `robots.txt`.
4. **OSINT → _Kidnapped part 1_** — search operators, reverse image search + Wayback.
5. **Forensics → _3D flag_** — identify and open the file.
6. **Reverse Engineering → _Love letter_** — `strings` the binary.

## ✅ Challenge

1. **Do:** Choose three highly-solved challenges from different categories and solve them.
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

Before competition day, complete the [On the Day Checklist](13-on-the-day.md).

🎉 **You've completed the course. Go capture some flags!**

⬅️ Back to the [Course Plan](../COURSE_PLAN.md) · [README](../README.md)
