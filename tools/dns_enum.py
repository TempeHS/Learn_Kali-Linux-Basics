#!/usr/bin/env python3
"""
dns_enum.py - Perform basic DNS Zone Transfer (AXFR) and Subdomain Brute Forcing.
Usage: python3 dns_enum.py target.com [--wordlist subdomains.txt]
"""
import sys
import argparse

try:
    import dns.resolver
    import dns.zone
    import dns.query
except ImportError:
    sys.exit("Please install dnspython: \n  Kali: sudo apt install python3-dnspython\n  pip:  pip install dnspython")

def test_axfr(domain):
    print(f"[*] Attempting Zone Transfer (AXFR) on {domain}...")
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        nameservers = [str(ns.target) for ns in ns_records]
    except Exception as e:
        print(f"[-] Could not resolve NS records: {e}")
        return

    axfr_success = False
    for ns in nameservers:
        print(f"[*] Trying NS: {ns}")
        try:
            # Resolve the IP of the nameserver first
            ns_ip = dns.resolver.resolve(ns, 'A')[0].to_text()
            # Attempt the zone transfer
            z = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain), check_origin=False)
            
            print(f"[+] AXFR successful against {ns}!")
            print(f"[+] Dumping Zone Data:")
            for name, node in z.nodes.items():
                print(f"    {z[name].to_text(name)}")
            axfr_success = True
            break
        except Exception as e:
            print(f"    [-] AXFR failed: {e}")
            
    if not axfr_success:
        print("[-] Zone transfer failed on all nameservers. They are secured.")

def brute_force(domain, wordlist_path):
    print(f"\n[*] Brute-forcing subdomains on {domain} using {wordlist_path}...")
    try:
        with open(wordlist_path, 'r') as f:
            subs = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Error reading wordlist: {e}")
        return
        
    found = []
    for sub in subs:
        target = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(target, 'A')
            ip_list = [a.to_text() for a in answers]
            print(f"[+] Found: {target} -> {ip_list}")
            found.append(target)
        except Exception:
            pass
            
    print(f"[*] Brute-force finished. Found {len(found)} subdomains.")

def main():
    parser = argparse.ArgumentParser(description="CTF DNS Enumeration Tool")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--wordlist", "-w", help="Path to a subdomain wordlist (optional)")
    args = parser.parse_args()

    test_axfr(args.domain)
    
    if args.wordlist:
        brute_force(args.domain, args.wordlist)

if __name__ == "__main__":
    main()