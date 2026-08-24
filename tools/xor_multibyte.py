#!/usr/bin/env python3
"""
xor_multibyte.py - Brute-force/crib-drag a multi-byte XOR key.
Usage: python3 xor_multibyte.py <hex_ciphertext> <known_crib>
"""
import sys

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <hex_ciphertext> <known_crib>")
        return
        
    ct = bytes.fromhex(sys.argv[1])
    crib = sys.argv[2].encode()
    
    print(f"[*] Ciphertext length: {len(ct)}")
    print(f"[*] Crib: {crib}")
    
    # Crib drag to find potential keys
    print("\n[*] Dragging crib...")
    for i in range(len(ct) - len(crib) + 1):
        ct_chunk = ct[i:i+len(crib)]
        key_chunk = xor_bytes(ct_chunk, crib)
        if all(32 <= b <= 126 for b in key_chunk):
            print(f" Offset {i:03d} | Potential key material > {key_chunk}")

if __name__ == "__main__":
    main()