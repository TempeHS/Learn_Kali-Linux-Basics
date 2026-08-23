# Advanced Reverse Engineering by Language

Use this side guide when a CTF challenge gives you a program written in a
language that is not covered by the main labs. Start with the common workflow,
then jump to the matching language.

## Quick menu

**Start here**

- [Identify the file type](#identify-the-file-type)
- [Use the universal workflow](#universal-workflow)
- [Install core Kali tools](#core-kali-tools)
- [Static versus dynamic analysis](#static-versus-dynamic-analysis)
- [Competition quick checklist](#competition-quick-checklist)

**Jump to a language or format**

| Challenge file               | Guide                                                    |
| ---------------------------- | -------------------------------------------------------- |
| `.class`, `.jar`             | [Java](#java-class-and-jar)                              |
| Native ELF or PE             | [C and C++](#c-and-c-native-elf-or-pe)                   |
| `.exe`, `.dll` with .NET/CLR | [C# and .NET](#c-and-net-exe-and-dll)                    |
| `.py`, `.pyc`, PyInstaller   | [Python](#python-source-bytecode-and-packaged-programs)  |
| `.js`, `.mjs`, `.cjs`        | [JavaScript and Node.js](#javascript-and-nodejs)         |
| Go native binary             | [Go](#go)                                                |
| Rust native binary           | [Rust](#rust)                                            |
| `.apk`                       | [Android Java and Kotlin](#android-java-and-kotlin-apks) |
| `.wasm`                      | [WebAssembly](#webassembly)                              |

> [!IMPORTANT]
> Only analyse files supplied by an authorised CTF or files you created. Do not
> run an unknown program just to see what happens. Inspect it statically first
> and use a disposable VM snapshot if you later need to run it.

## Identify the file type

File extensions are clues, but `file` and the file header are more reliable.

| What `file` or the extension shows | Likely format or language | Start with                             |
| ---------------------------------- | ------------------------- | -------------------------------------- |
| `ELF ... executable`               | C, C++, Go or Rust        | `readelf`, `nm`, Ghidra, radare2       |
| `PE32` or `PE32+`                  | Windows C/C++ or C#       | `strings`, Ghidra; then check for .NET |
| `.class` or `.jar`                 | Java bytecode             | `javap`, JADX                          |
| `.apk`                             | Android Java/Kotlin       | JADX, `apktool`                        |
| `.exe` or `.dll` with CLR metadata | C#/.NET                   | ILSpy, `monodis`                       |
| `.py`, `.pyc` or PyInstaller       | Python                    | `dis`, a compatible Python decompiler  |
| `.js`, `.mjs` or `.cjs`            | JavaScript                | a formatter, text search, source maps  |
| `WebAssembly` or `.wasm`           | WebAssembly               | `wasm2wat`                             |

Useful header checks:

```bash
file challenge
xxd -l 16 challenge
readelf -h challenge 2>/dev/null | head
objdump -f challenge 2>/dev/null | head
```

Once you know the format, use the menu above to jump straight to its tools.

## Universal workflow

1. Save the original file and calculate its hash.
2. Identify its file type, architecture and likely language.
3. Try `strings` before opening a decompiler.
4. Decompile or disassemble it with the language-specific tool.
5. Find the entry point and trace comparisons, decoding and flag-building code.
6. Run it only if static analysis is not enough.
7. Record commands and discoveries for your team.

Make a working copy so you do not accidentally change the original:

```bash
sha256sum challenge
cp challenge challenge-working
file challenge-working
strings -n 6 challenge-working | head -n 40
```

## Core Kali tools

Refresh APT metadata before searching for or installing packages:

```bash
sudo apt update
sudo apt install -y file unzip p7zip-full binutils gdb radare2 ghidra
```

Confirm each tool before the competition:

```bash
for tool in file strings objdump gdb radare2 ghidra; do
  command -v "$tool" || echo "MISSING: $tool"
done
```

If APT says a package cannot be found, check the spelling and your configured
repositories with `apt-cache search TOOL`. Do not download a similarly named
binary from an untrusted website.

## Java: `.class` and `.jar`

### Install Java and JADX

The JDK supplies `java`, `jar` and `javap`. JADX turns Java bytecode back into
readable Java-like source.

```bash
sudo apt update
sudo apt install -y default-jdk jadx
java -version
javap -version
jadx --version
```

You need the JDK, not only a Java Runtime Environment, because `javap` is a JDK
tool.

### Inspect a JAR without running it

```bash
file challenge.jar
unzip -l challenge.jar | head -n 40
unzip -p challenge.jar META-INF/MANIFEST.MF 2>/dev/null
strings -n 6 challenge.jar | grep -Ei "pecan|flag|secret|password"
```

The manifest may contain a line such as `Main-Class: ctf.Main`. That class is
the program's entry point.

List classes and disassemble the entry point with `javap`:

```bash
jar tf challenge.jar | grep '\.class$' | head -n 40
javap -classpath challenge.jar -c -p ctf.Main | less
```

Replace `ctf.Main` with the class from the manifest. In `javap` output, look for
string constants, calls to `equals`, loops over byte arrays and methods with
names such as `check`, `decode` or `verify`.

### Decompile with JADX

```bash
rm -rf java-output
jadx -d java-output challenge.jar
grep -RniE "pecan|flag|secret|password|equals|decode" java-output
```

For a GUI, run `jadx-gui challenge.jar`. Start at the manifest's main class,
then follow methods that process user input. Compiler-generated variable names
may be imperfect, but strings and control flow are usually clear.

### Run only when necessary

After static inspection, use a disposable VM and a time limit:

```bash
timeout 15s java -jar challenge.jar
```

A JAR can run commands, access files and use the network. Java bytecode is not
safe merely because it is easy to decompile.

## C and C++: native ELF or PE files

Install the native toolchain if it is not already present:

```bash
sudo apt update
sudo apt install -y build-essential binutils gdb radare2 ghidra
```

Start with:

```bash
file challenge
readelf -h challenge | less
strings -n 6 challenge | grep -Ei "pecan|flag|correct|wrong|password"
nm -C challenge 2>/dev/null | less
objdump -d -M intel challenge | less
```

`nm -C` converts many C++ mangled names back into readable names. If it prints
`no symbols`, the binary is stripped; use its strings, imports and control flow
in Ghidra or radare2 instead.

A quick radare2 session:

```bash
radare2 -A challenge
```

At the prompt, use `afl` to list functions, `izz` to list strings, `axt @ ADDRESS`
to find references to a string and `pdf @ main` to view `main`. Enter `q` to
quit.

In Ghidra:

1. Start `ghidra` and create a non-shared project.
2. Import the challenge file and accept the detected format and architecture.
3. Open it in CodeBrowser and run Auto Analyze.
4. Open **Window > Defined Strings** and find success/failure messages.
5. Follow references to those strings and read the Decompiler window.
6. Rename functions and variables as their purpose becomes clear.

Use GDB only after static analysis:

```bash
gdb -q ./challenge
```

Useful GDB commands are `break main`, `run`, `next`, `step`, `info registers`,
`x/s ADDRESS` and `quit`.

## C# and .NET: `.exe` and `.dll`

A C# program is commonly a Windows PE file containing CLR/.NET metadata. Check
before assuming every `.exe` is native code:

```bash
file challenge.exe
strings -el challenge.exe | grep -Ei "pecan|flag|secret|password"
```

The `-el` option searches little-endian UTF-16 strings, which are common in
Windows and .NET programs.

### Install Mono inspection tools

```bash
sudo apt update
sudo apt install -y mono-devel mono-utils
mono --version
monodis --assembly challenge.exe
monodis --typedef challenge.exe
monodis challenge.exe | less
```

`monodis` displays .NET Intermediate Language (IL). Look for the entry point,
`ldstr` string-loading instructions, comparison calls and methods that transform
arrays or text.

### Decompile to C# with ILSpy

ILSpy's command-line tool requires a .NET SDK. First see which SDK Kali offers:

```bash
apt-cache search '^dotnet-sdk-[0-9]'
```

Install one of the listed SDK packages, then install ILSpy as a user tool:

```bash
dotnet tool install --global ilspycmd
export PATH="$PATH:$HOME/.dotnet/tools"
ilspycmd --version
ilspycmd -p -o csharp-output challenge.exe
grep -RniE "pecan|flag|secret|password|correct" csharp-output
```

If Kali offers no .NET SDK package, use the current official Microsoft .NET
installation instructions rather than adding an unofficial repository. Mono's
`monodis` still provides a static-analysis path without ILSpy.

Run older .NET Framework programs with `mono challenge.exe` only inside a
disposable VM. Modern .NET programs may instead require `dotnet challenge.dll`.

## Python: source, bytecode and packaged programs

Plain `.py` files are source code. Format them and search them directly:

```bash
python3 -m py_compile challenge.py
python3 -m dis challenge.py | less
grep -nEi "pecan|flag|secret|password|decode" challenge.py
```

For `.pyc`, first identify the bytecode version:

```bash
file challenge.pyc
strings -n 6 challenge.pyc | head -n 40
```

Python bytecode changes between versions, so a decompiler must support the
version that created the file. Install isolated Python tools with `pipx`:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
pipx install decompyle3
```

Then try `decompyle3 challenge.pyc`. If it reports an unsupported bytecode
version, record that version and use a compatible interpreter/decompiler rather
than repeatedly modifying the file.

A PyInstaller executable is still a native executable containing a Python
archive. `file`, `strings` and Ghidra remain useful even when extraction tools
do not recognise its version.

## JavaScript and Node.js

JavaScript is normally distributed as source, though it may be minified or
obfuscated.

```bash
sudo apt update
sudo apt install -y nodejs npm
node --version
npx prettier challenge.js

grep -nEi "pecan|flag|secret|password|atob|fromCharCode|eval" challenge.js
find . -name '*.map' -o -name '*.wasm'
```

Source-map (`.map`) files can contain original filenames and readable source.
Treat `eval`, long encoded strings and arrays of character codes as leads. Do
not run an unknown script with `node` until you have inspected its imports,
file access, child processes and network calls.

### WebAssembly

For WebAssembly, install the WebAssembly Binary Toolkit if Kali offers it:

```bash
apt-cache search wabt
sudo apt install -y wabt
wasm2wat module.wasm -o module.wat
```

The generated `.wat` file is text that can be searched and read.

## Go

Go usually compiles to a native ELF or PE file, so use the C/C++ workflow first.
Go binaries are often large because they include runtime code.

```bash
file challenge
strings -n 8 challenge | grep -Ei "pecan|flag|correct|wrong"
nm -C challenge 2>/dev/null | less
readelf -p .comment challenge 2>/dev/null
```

Go binaries often retain package paths and names such as `main.main`. Focus on
the program's own `main`, input-handling and comparison functions instead of
reading runtime functions.

The compiler is only needed if a challenge asks you to modify or rebuild code:

```bash
sudo apt update
sudo apt install -y golang-go
```

## Rust

Rust also compiles to native ELF or PE files, so begin with the C/C++ workflow.
Names may be long or mangled; `nm -C` and Ghidra can demangle many of them.

```bash
file challenge
strings -n 8 challenge | grep -Ei "pecan|flag|correct|wrong"
nm -C challenge 2>/dev/null | less
readelf -p .comment challenge 2>/dev/null
```

Focus on the program's input-handling and comparison functions instead of the
Rust runtime. Install the compiler only when a challenge requires rebuilding:

```bash
sudo apt update
sudo apt install -y rustc cargo
```

## Android Java and Kotlin APKs

An APK is a ZIP archive containing Android resources and Dalvik bytecode. JADX
usually provides the fastest path to Java/Kotlin-like source; `apktool` exposes
resources and smali assembly.

```bash
sudo apt update
sudo apt install -y jadx apktool
file challenge.apk
unzip -l challenge.apk | head -n 40
jadx -d apk-output challenge.apk
apktool d challenge.apk -o apktool-output
grep -RniE "pecan|flag|secret|password" apk-output apktool-output
```

Check `AndroidManifest.xml` for the starting activity and permissions, then
trace that activity in JADX. Do not install an unknown APK on your personal
phone.

## Static versus dynamic analysis

**Static analysis** reads a program without running it: `strings`, `javap`,
JADX, `monodis`, Ghidra and `objdump`. Always start here.

**Dynamic analysis** observes a running program: GDB, `strace`, `ltrace`, Java,
Mono or Node. Use it only in a disposable VM after static inspection. Take a VM
snapshot, disconnect networking unless the challenge needs it and never provide
real credentials or personal files.

Useful Linux tracing tools for native programs:

```bash
sudo apt install -y strace ltrace
strace -f -o strace.log ./challenge
ltrace -o ltrace.log ./challenge
```

Tracing executes the program, so the same safety rules apply.

## Competition quick checklist

```text
[ ] Hash and copy the original file
[ ] Run file, strings and a header check
[ ] Identify native code, Java, .NET, Python, JavaScript or Android
[ ] Find the entry point
[ ] Search strings and follow their references
[ ] Trace input to the success/failure comparison
[ ] Record commands and clues for the team
[ ] Run only in a disposable environment if static analysis is insufficient
```

Return to [Lesson 08](labs/08-reverse-engineering.md) for the beginner ELF
workflow or the [CTF competition playbook](labs/11-ctf-competition.md) for
triage and team handoffs.
