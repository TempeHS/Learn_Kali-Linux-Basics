# AI Prompt Guide for CTF Learning

Use this guide to ask AI for explanations, hints and debugging help while **you**
do the investigation. The goal is to understand the challenge and learn a
technique, not to ask AI to produce a flag.

> [!IMPORTANT]
> AI rules are specific to each competition. Always read the official rules;
> they override this guide. If the rules do not explicitly allow AI, assume
> **AI is not allowed**. If anything is unclear, ask an organiser and do not use
> AI until they confirm it is permitted. This guide describes common rules for
> competitions that do allow limited AI assistance; it does not grant permission
> to use AI in any particular event.

## Quick menu

- [Before you ask](#before-you-ask)
- [Build a useful prompt](#build-a-useful-prompt)
- [Understand a challenge](#understand-a-challenge)
- [Learn how something works](#learn-how-something-works)
- [Choose a tool or next check](#choose-a-tool-or-next-check)
- [Understand a command](#understand-a-command)
- [Fix an error](#fix-an-error)
- [Get help with your code](#get-help-with-your-code)
- [Interpret output](#interpret-output)
- [Ask for a small hint](#ask-for-a-small-hint)
- [Check your reasoning](#check-your-reasoning)
- [Prompts by CTF category](#prompts-by-ctf-category)
- [Prompts to avoid](#prompts-to-avoid)

## Before you ask

Use AI only after you have read the challenge and tried at least one sensible
check yourself.

Do not share:

- Flags or partial flags.
- Competition-only files or the complete challenge statement.
- Passwords, tokens, cookies or credentials.
- Personal information about students, organisers or other people.
- Private URLs, source code or data that the rules prohibit sharing.

Share the **minimum useful detail** instead: the file type, the command you ran,
a short non-sensitive error, and what you think it means.

## Build a useful prompt

A good learning prompt has five parts:

```text
Context: I am a first-time student in an authorised CTF.
Goal: Explain or help me investigate one specific thing.
What I tried: Include my command or reasoning.
Evidence: Include a short, non-sensitive output or error.
Boundary: Do not solve the challenge or provide a flag. Give one next step and
explain why it is useful.
```

You can copy this shorter template:

```text
I am solving an authorised CTF challenge. I think this is [CATEGORY] because
[EVIDENCE]. I tried [COMMAND OR METHOD] and observed [SHORT OUTPUT]. Explain
what this suggests and give me one next check. Do not solve the challenge or
provide a flag.
```

## Understand a challenge

Use this when the wording is confusing:

```text
Explain these terms at high-school level: [TERMS]. Describe what skill each
term points to, but do not solve a challenge or produce a flag.
```

```text
I received a [FILE TYPE / SHORT CLUE] in an authorised CTF. What questions
should I ask myself to identify the category? Give me a checklist, not a
solution.
```

```text
Without solving anything, explain what the phrase [SHORT PHRASE] might mean in
cryptography / forensics / web / OSINT / reverse engineering. Give two possible
interpretations and a way I could distinguish between them.
```

## Learn how something works

Use AI as a tutor before applying a technique:

```text
Explain how [BASE64 / XOR / EXIF / DNS / HTTP / FILE SIGNATURES] works at
high-school level. Use a small made-up example unrelated to any competition.
Then ask me one question to check my understanding.
```

```text
Teach me the difference between [TWO CONCEPTS], such as encoding and encryption.
Include when each appears in a beginner CTF and one harmless practice example.
```

```text
Explain what happens internally when I run [COMMAND]. Describe its input,
output and common mistakes. Do not apply it to a competition challenge for me.
```

## Choose a tool or next check

Describe evidence instead of asking for an answer:

```text
In an authorised CTF, `file` reports [SHORT FILE DESCRIPTION]. Which two Kali
tools are appropriate for an initial static inspection? Explain what evidence
each tool could reveal. Do not analyse the file or solve the challenge.
```

```text
I tried [FIRST CHECK] on a [FILE TYPE], but it showed [SHORT RESULT]. Suggest
one different next check and explain what result would support or reject my
current idea: [HYPOTHESIS].
```

```text
Compare [TOOL A] and [TOOL B] for [TASK]. Which is easier for a beginner, and
what are the limitations of each?
```

## Understand a command

```text
Break down this command one part at a time:
[COMMAND]
Explain every option, what files it may create and whether it executes the
input. Do not run it or extend it into a challenge solution.
```

```text
Rewrite this command as a sequence of simpler commands so I can inspect the
output after each step:
[COMMAND]
Explain what I should learn from each step.
```

```text
What safety risks should I consider before running this command on an unknown
CTF file?
[COMMAND]
Suggest a static-analysis alternative if one exists.
```

## Fix an error

Include the exact command and only the relevant error lines:

```text
On Kali Linux I ran:
[COMMAND]

It returned:
[SHORT ERROR]

Explain the likely cause, give one diagnostic check, and wait for its result
before suggesting more. Do not solve the CTF challenge.
```

```text
This command worked differently from the lesson:
[COMMAND]
Expected: [EXPECTED BEHAVIOUR]
Observed: [OBSERVED BEHAVIOUR]

List the two most likely causes and the quickest check that distinguishes them.
```

Never paste a password, API key or session cookie when showing an error.
Replace sensitive values with `[REDACTED]`.

## Get help with your code

AI may help explain or correct a small script that **you wrote**:

```text
I wrote this small script for an authorised CTF:
[SMALL CODE EXCERPT]

I expected [BEHAVIOUR], but observed [RESULT]. Identify the bug and explain the
smallest correction. Do not add code that completes the challenge or extracts
a flag.
```

```text
Review this function for an off-by-one error and explain how I can test it with
made-up input. Do not rewrite the whole program:
[FUNCTION]
```

```text
Explain this unfamiliar line of Java / C++ / C# / Python code:
[ONE OR TWO LINES]
What values go in, what value comes out, and what harmless test could confirm
that explanation?
```

## Interpret output

Do not paste huge output. Select a few relevant lines and remove sensitive data.

```text
I ran [COMMAND] on an authorised CTF file and received these lines:
[SHORT OUTPUT]

Explain what each line means. Which line is the strongest lead, and what one
command could test that lead? Do not decode or recover the flag for me.
```

```text
Does this output support my hypothesis that the file is [FORMAT / LANGUAGE]?
[SHORT OUTPUT]
Explain the evidence for and against my hypothesis, then suggest one confirming
check.
```

## Ask for a small hint

Use a hint ladder so AI does not jump to the solution:

```text
I am stuck after trying [ATTEMPTS]. Give only a level 1 hint: point me toward a
concept or tool, but do not give a command, procedure, answer or flag.
```

If that is not enough:

```text
Give a level 2 hint for the same problem: suggest one check I can perform, but
do not interpret its result or provide the answer.
```

Only if the rules allow more help:

```text
Explain how to perform that check using a small invented example unrelated to
the challenge. I will apply and verify it myself.
```

## Check your reasoning

```text
My hypothesis is: [HYPOTHESIS].
My evidence is: [SHORT EVIDENCE].
My next check is: [CHECK].

Do not solve the challenge. Point out one unsupported assumption and tell me
what result would falsify my hypothesis.
```

```text
Here is my explanation of how [CONCEPT] works:
[YOUR EXPLANATION]

Correct any misunderstanding using a made-up example. Do not discuss a specific
competition answer.
```

```text
I believe I solved this step using [TECHNIQUE], but I will not share the flag.
Ask me three questions that check whether I understand why the technique worked.
```

## Prompts by CTF category

### Cryptography and encoding

```text
This text has the visible pattern [CHARACTER SET / LENGTH / PADDING], with the
actual value omitted. What encodings or ciphers commonly have that pattern?
Give two identification checks, not a decode or answer.
```

```text
Explain how to recognise Base64, hexadecimal and a Caesar shift without using
my challenge data. Include one false positive to watch for.
```

### OSINT

```text
I have a public clue of type [PHOTO / PLACE NAME / DATE / DOMAIN]. Build a legal
OSINT research plan using public sources. Do not identify the person or place
for me; give search questions and ways to confirm evidence.
```

```text
Explain how to verify a location hypothesis with two independent public clues.
Use an invented example and include a warning about unreliable metadata.
```

Do not ask AI to identify a private person, infer sensitive personal details or
bypass access controls.

### Web

```text
On an authorised practice site, I observed HTTP status [CODE] after requesting
[NON-SENSITIVE PATH TYPE]. Explain what that status means and one normal browser
or `curl` check I can make next. Do not provide an exploit or flag.
```

```text
Explain the purpose of `robots.txt`, HTML comments and response headers in a
beginner web CTF. Use an invented website, not the competition target.
```

### Steganography and forensics

```text
I have a [FILE TYPE]. `file` reports [DESCRIPTION], and `exiftool` reports
[SHORT NON-SENSITIVE RESULT]. What does this rule out, and which one static
check should I try next? Do not extract hidden content for me.
```

```text
Explain the difference between metadata, appended data and embedded files. Show
how each would appear in harmless sample output.
```

### Reverse engineering

```text
`file` identifies the challenge as [ELF / PE / JAR / .NET / PYTHON]. Explain the
usual entry point and the best static-analysis tool for that format. Give a
navigation checklist, not a solution.
```

```text
Explain this short decompiler excerpt at a high level:
[SMALL EXCERPT]
Describe its inputs, branches and output without calculating any competition
secret or rewriting the complete algorithm.
```

### Linux and networking

```text
Explain the difference between [TWO COMMANDS OR PROTOCOLS] and when each is
appropriate in an authorised CTF. Include a harmless localhost example.
```

```text
I received this short Nmap result from an authorised target:
[REDACTED OUTPUT]
Explain the columns and suggest one non-intrusive follow-up check. Do not suggest
attacking unrelated systems.
```

## Prompts to avoid

Do not use prompts such as:

```text
Solve this challenge for me.
```

```text
Here is the complete challenge and file. Find the flag.
```

```text
Write a script that automatically attacks every target and submits answers.
```

```text
Tell me exactly what commands to run from start to finish.
```

Replace them with prompts that request **one explanation, one hint or one check**:

```text
I tried [METHOD] and observed [RESULT]. Explain the concept I may be missing and
give one small next check. Do not solve the challenge or provide a flag.
```

## The final test

Before using an AI response, ask yourself:

1. Can I explain why this step makes sense?
2. Have I run and verified it myself?
3. Am I following the competition rules?
4. Could I describe my work to a teammate without saying "the AI solved it"?

If not, stop and learn the missing concept before submitting anything.

Return to the [CTF competition playbook](labs/11-ctf-competition.md) or the
[On the Day Checklist](labs/13-on-the-day.md).
