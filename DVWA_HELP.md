# DVWA Help Guide

Use this guide when a lab mentions the built-in DVWA target.

## What DVWA Is (in this repo)

This project includes a built-in **DVWA** (Damn Vulnerable Web Application)
container for safe, legal practice inside your dev environment.

- From the Kali terminal: `http://dvwa`
- From your browser tab: `http://localhost:4280`

Use only this target (or systems you own/have permission to test).

## Quick Start

1. Open `http://localhost:4280` in your browser.
2. Log in with `admin` / `password`.
3. Open **DVWA Security** and set security to **Low**.
4. If it is a new container, open **Setup** and click
   **Create / Reset Database** once.

## Troubleshooting

### Fatal error / database connection refused

The app likely started before MySQL was ready.

1. Open `http://localhost:4280/setup.php`.
2. Click **Create / Reset Database**.
3. If setup fails, rebuild the dev container so `db` restarts.

### Cannot open localhost:4280

- In VS Code, check the **Ports** tab.
- Ensure port **4280** is forwarded and open it from there.

### Login fails

- Use `admin` / `password`.
- If it still fails, reset the database on `setup.php`.

### Terminal says could not resolve host: dvwa

`dvwa` only resolves inside the dev container.

- Run commands from the VS Code terminal attached to this repo.
- If needed, rebuild the dev container.

### sqlmap/curl says not logged in

DVWA vulnerable pages require an authenticated session.

1. Log in via browser.
2. Copy your `PHPSESSID` cookie value from DevTools.
3. Pass it in requests, for example:

```bash
sqlmap -u "http://dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=<PHPSESSID>; security=low" \
  --batch --level=1 --risk=1
```

## Health Check (from terminal)

```bash
curl -s http://dvwa/login.php | grep -q user_token && echo "DVWA OK" || echo "DVWA database not ready"
```

If this prints `DVWA database not ready`, run the setup reset step above.
