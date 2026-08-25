#!/usr/bin/env bash
# Runs once when the codespace/container is created (see devcontainer.json).
# Deliberately non-fatal: a failure here should never block a student from
# getting a working shell.

set -u

cd "$(dirname "$0")/.." || exit 0
REPO="$PWD"

# Python packages used by the lab scripts and by the `lab` / `show` commands.
pip3 install --break-system-packages -r requirements.txt ||
    pip3 install -r requirements.txt

# Hook the shell improvements into bash, once.
if ! grep -qF 'student-shell.sh' "$HOME/.bashrc" 2>/dev/null; then
    printf '\n# Cyber Security course shell improvements (readable source in the repo)\n[ -f "%s/.devcontainer/student-shell.sh" ] && . "%s/.devcontainer/student-shell.sh"\n' \
        "$REPO" "$REPO" >>"$HOME/.bashrc"
fi

# Download the tldr example pages so `tldr nmap` works offline.
command -v tldr >/dev/null 2>&1 && tldr --update >/dev/null 2>&1

exit 0
