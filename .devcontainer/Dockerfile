# Kali Linux learning environment for high school Cyber Security students.
# Based on the official Kali rolling image with a curated (not overboard)
# set of beginner-friendly security tools.
FROM kalilinux/kali-rolling

# Avoid interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install a curated toolkit.
# These tools cover the core beginner skills: the Linux command line,
# network discovery, web reconnaissance, password basics and scripting.
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Core shell & quality-of-life ---
    sudo \
    bash \
    bash-completion \
    nano \
    vim \
    less \
    tree \
    man-db \
    manpages \
    # Beginner-friendly, example-first summaries of commands: `tldr nmap`
    tealdeer \
    # Read and filter JSON from the web-recon labs
    jq \
    git \
    curl \
    wget \
    unzip \
    ca-certificates \
    # --- Scripting (used in lab exercises) ---
    python3 \
    python3-pip \
    python3-venv \
    # --- Networking basics ---
    net-tools \
    iputils-ping \
    iproute2 \
    dnsutils \
    whois \
    traceroute \
    netcat-traditional \
    tcpdump \
    # --- Reconnaissance & scanning ---
    nmap \
    # --- Web application testing ---
    nikto \
    dirb \
    gobuster \
    sqlmap \
    whatweb \
    # --- Password / hashing basics ---
    john \
    hydra \
    hashid \
    # --- Packet analysis (CLI) ---
    tshark \
    # --- Encoding / crypto helpers (CyberChef-style work in the terminal) ---
    openssl \
    xxd \
    # --- Forensics & steganography (CTF categories) ---
    file \
    binutils \
    binwalk \
    foremost \
    libimage-exiftool-perl \
    steghide \
    imagemagick \
    pngcheck \
    # --- Reverse engineering basics (CTF category) ---
    gdb \
    radare2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Codespaces mounts the container filesystem with no_new_privs, which blocks
# executing binaries that carry Linux file capabilities. Kali's nmap package
# sets cap_net_raw on its helper binary, so we strip it here; TCP connect
# scans (nmap -sT) still work perfectly for learning.
RUN setcap -r /usr/lib/nmap/nmap 2>/dev/null || true

# Create a non-root "student" user with passwordless sudo so learners can
# practise safely. Working as a normal user (not root) is itself a good habit.
ARG USERNAME=student
RUN useradd -m -s /bin/bash ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}

CMD ["/bin/bash"]
