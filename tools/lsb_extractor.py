#!/usr/bin/env python3
"""
lsb_extractor.py - Extract Least Significant Bits from image pixels.
Usage: python3 lsb_extractor.py <image.png>
"""
import sys
try:
    from PIL import Image
except ImportError:
    sys.exit("Please install Pillow: pip install Pillow")

def extract_lsb(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    extracted_bits = []
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            extracted_bits.append(r & 1)
            extracted_bits.append(g & 1)
            extracted_bits.append(b & 1)
            
    # Reassemble bits into bytes
    extracted_bytes = bytearray()
    for i in range(0, len(extracted_bits), 8):
        byte = 0
        for bit in extracted_bits[i:i+8]:
            byte = (byte << 1) | bit
        extracted_bytes.append(byte)
        
    return extracted_bytes

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image_file>")
        return
        
    img_path = sys.argv[1]
    print(f"[*] Extracting LSB from {img_path}...")
    
    data = extract_lsb(img_path)
    
    # Save raw bytes
    out_file = "lsb_extracted.bin"
    with open(out_file, "wb") as f:
        f.write(data)
    print(f"[+] Saved raw binary to {out_file}")
    
    # Try hunting for text strings in the first few kilobytes
    print("[*] Sneak peek of printable strings:")
    import re
    strings = re.findall(b"[ -~]{5,}", data[:4096])
    for s in strings:
        print(f"    {s.decode()}")

if __name__ == "__main__":
    main()