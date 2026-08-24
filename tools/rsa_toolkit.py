#!/usr/bin/env python3
"""
rsa_toolkit.py - Automate basic RSA decryption using FactorDB.
Usage: python3 rsa_toolkit.py <n> <e> <c>
"""
import sys
import requests

def egcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise Exception('Modular inverse does not exist')
    return x % m

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <n> <e> <c>")
        return
        
    n = int(sys.argv[1])
    e = int(sys.argv[2])
    c = int(sys.argv[3])
    
    print(f"[*] Querying FactorDB for n = {n}")
    resp = requests.get(f"http://factordb.com/api?query={n}")
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get('status') == 'FF':
            factors = [int(f[0]) for f in data.get('factors', []) for _ in range(f[1])]
            if len(factors) == 2:
                p, q = factors
                print(f"[+] Found factors! p={p}, q={q}")
                phi = (p - 1) * (q - 1)
                d = modinv(e, phi)
                print(f"[*] Calculated private key d = {d}")
                m = pow(c, d, n)
                print(f"[*] Decrypted int: {m}")
                try:
                    pt = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
                    print(f"[+] Plaintext: {pt}")
                except:
                    print("[!] Could not decode plaintext as ASCII")
            else:
                print("[-] n has more/less than 2 factors, not basic RSA.")
        else:
            print("[-] FactorDB did not have full factors for n.")
    else:
        print("[-] Error reaching FactorDB")

if __name__ == "__main__":
    main()