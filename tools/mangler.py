#!/usr/bin/env python3
"""
mangler.py - Generate password permutations based on base words for CTF cracking.
Usage: python3 mangler.py <words.txt>
"""
import sys

YEARS = ["2023", "2024", "2025", "2026", "1"]
SYMBOLS = ["!", "@", "#", "$", "?"]
LEET_DICT = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '1'}

def leet_speak(word):
    res = word.lower()
    for k, v in LEET_DICT.items():
        res = res.replace(k, v)
    return res

def mangle_word(word):
    word = word.strip()
    if not word: return []
    
    variations = {
        word.lower(),
        word.upper(),
        word.capitalize()
    }
    
    # Add leetspeak variation
    variations.add(leet_speak(word))
    variations.add(leet_speak(word).capitalize())
    
    # Append years and symbols
    extended_variations = set(variations)
    for v in variations:
        for y in YEARS:
            extended_variations.add(v + y)
            for s in SYMBOLS:
                extended_variations.add(v + s)
                extended_variations.add(v + y + s)
                extended_variations.add(v + s + y)
                
    return extended_variations

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <base_words_file>")
        return
        
    try:
        with open(sys.argv[1], "r") as f:
            words = f.readlines()
    except Exception as e:
        print(f"[-] Error opening file: {e}")
        return
        
    result_set = set()
    for w in words:
        result_set.update(mangle_word(w))
        
    out_file = "mangled_wordlist.txt"
    with open(out_file, "w") as f:
        for word in sorted(result_set):
            f.write(word + "\n")
            
    print(f"[+] Loaded {len(words)} base words.")
    print(f"[+] Generated {len(result_set)} permutations.")
    print(f"[+] Saved to {out_file}.")

if __name__ == "__main__":
    main()