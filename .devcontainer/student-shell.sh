# student-shell.sh - small, readable shell improvements for learners.
#
# Sourced from ~/.bashrc. Read it! Everything here is plain bash that you
# could type yourself. Nothing is hidden and no real command is replaced by a
# different program, so every skill you build here transfers to any Linux box.

# ---------------------------------------------------------------------------
# 1. Show the exit status of the last command in the prompt.
#
# Every command returns a number: 0 means success, anything else is an error.
# Beginners usually never notice a command failed. Now you cannot miss it.
# You can always check it yourself the normal way with:  echo $?
# ---------------------------------------------------------------------------
__student_exit_flag() {
    local code=$?
    # \001 and \002 tell bash these bytes are invisible, so line-wrapping works.
    if ((code == 0)); then
        printf '\001\e[0;32m\002[ok]\001\e[0m\002 '
    else
        printf '\001\e[0;31m\002[exit %d]\001\e[0m\002 ' "$code"
    fi
}

case "$PS1" in
*__student_exit_flag*) ;; # already applied, don't stack it twice
*) PS1='$(__student_exit_flag)'"$PS1" ;;
esac

# ---------------------------------------------------------------------------
# 2. Make man pages readable.
#
# man pages are the single most transferable skill in this course, but the
# default all-grey rendering is hard to scan. These variables colour the bits
# groff marks as bold (commands) and underlined (options/arguments).
# GROFF_NO_SGR is required on Debian/Kali for this to take effect.
# ---------------------------------------------------------------------------
export GROFF_NO_SGR=1
export LESS_TERMCAP_md=$'\e[1;36m' # bold      -> cyan   (headings, commands)
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;33m' # underline -> yellow (options, arguments)
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_so=$'\e[1;44;37m' # standout -> status bar / search hits
export LESS_TERMCAP_se=$'\e[0m'

# -R keeps colour when a tool pipes into less; -F skips the pager for short output.
export LESS='-R -F -X'

# ---------------------------------------------------------------------------
# 3. Safer, more useful history.
# ---------------------------------------------------------------------------
HISTSIZE=5000
HISTFILESIZE=10000
HISTTIMEFORMAT='%F %T  ' # `history` now shows when you ran each command
shopt -s histverify      # `!!` / `!nmap` load onto the prompt for review first

# ---------------------------------------------------------------------------
# 4. `lab` - read a lab worksheet in the terminal, nicely rendered.
# 5. `show` - read a script with syntax highlighting and line numbers.
#
# Both use the Rich library's built-in command line renderers. Try them
# directly:  python3 -m rich.markdown --help
# Each falls back to a standard tool if Rich is missing, so nothing breaks.
# ---------------------------------------------------------------------------
__STUDENT_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

lab() {
    local dir="$__STUDENT_REPO/labs" match

    if [[ -z ${1:-} ]]; then
        echo "Labs in $dir:"
        command ls -1 "$dir"
        echo
        echo "Usage: lab 05      # opens 05-web-recon.md"
        return 0
    fi

    match=$(command ls -1 "$dir" | grep -m1 -i -- "$1")
    if [[ -z $match ]]; then
        echo "No lab matching '$1'. Run 'lab' to list them." >&2
        return 1
    fi

    python3 -m rich.markdown --page "$dir/$match" 2>/dev/null ||
        less "$dir/$match"
}

show() {
    if [[ -z ${1:-} ]]; then
        echo "Usage: show tools/dns_enum.py    # code, with line numbers" >&2
        return 1
    fi

    python3 -m rich.syntax --line-numbers --indent-guides "$1" 2>/dev/null ||
        cat "$1"
}
