import sys
import os
import pytest

# Add tools directory to Python path so we can import the scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')))

from xor_multibyte import xor_bytes
from rsa_toolkit import egcd, modinv
from mangler import leet_speak, mangle_word
from ctf_peel import try_base64, try_rot13

# -- Tests for xor_multibyte.py --
def test_xor_bytes():
    # 'A' (65) XOR 'B' (66) = 3
    assert xor_bytes(b'A', b'B') == bytes([3])
    # xor against null bytes yields original
    assert xor_bytes(b'hello', b'\x00' * 5) == b'hello'

# -- Tests for rsa_toolkit.py --
def test_egcd():
    g, x, y = egcd(10, 15)
    assert g == 5
    assert (10 * x) + (15 * y) == 5

def test_modinv():
    # 3 * 4 = 12, 12 mod 11 = 1. So modinv of 3 under mod 11 is 4.
    assert modinv(3, 11) == 4
    
    # Inverse doesn't exist when there's a common factor
    with pytest.raises(Exception):
        modinv(2, 4)

# -- Tests for mangler.py --
def test_leet_speak():
    assert leet_speak('hello') == 'h3110'
    assert leet_speak('password') == 'p@$$w0rd'
    
def test_mangle_word():
    variations = set(mangle_word('test'))
    
    # Check casing variations
    assert 'test' in variations
    assert 'TEST' in variations
    assert 'Test' in variations
    
    # Check leetspeak
    assert 't3$t' in variations
    
    # Check year appending
    assert 'test2024' in variations
    
    # Check complex mangling (leet + symbol + year)
    assert 't3$t2024!' in variations
    assert 'Test@2025' in variations

# -- Tests for ctf_peel.py --
def test_try_base64():
    import base64
    original = b"this is a secret ctf string"
    encoded = base64.b64encode(original)
    
    # verify try_base64 can decode it back directly
    assert try_base64(encoded) == original

def test_try_rot13():
    original = b"hello ctf player"
    encoded = b"uryyb pgS cynlre"
    # Note: rot13 preserves casing. 'S' -> 'F', so we get 'hello ctF player'. 
    # Updating original to match the correct output of rot_13
    assert try_rot13(encoded) == b"hello ctF player"

# -- Tests for lsb_extractor.py --
def test_lsb_extractor(tmp_path):
    try:
        from PIL import Image
    except ImportError:
        pytest.xfail("Pillow is not installed. To run this test, install via: sudo apt install python3-pil")
        
    from lsb_extractor import extract_lsb
    
    # Create a tiny 3x1 image (3 pixels, 9 color channels)
    img = Image.new('RGB', (3, 1))
    pixels = img.load()
    
    # We will hide the binary sequence 10101011 (171 or 0xAB) using RGB LSBs
    # Pixel 1: R=1, G=0, B=1
    pixels[0, 0] = (255, 254, 255)
    # Pixel 2: R=0, G=1, B=0
    pixels[1, 0] = (254, 255, 254)
    # Pixel 3: R=1, G=1, B=0 (The 9th bit is a zero)
    pixels[2, 0] = (255, 255, 254)
    
    img_path = str(tmp_path / "test_lsb.png")
    img.save(img_path)
    
    extracted = extract_lsb(img_path)
    
    # Check that the first assembled byte is exactly 0xAB (10101011 in binary)
    assert len(extracted) == 2 
    assert extracted[0] == 0xAB

# -- Tests for dns_enum.py --
def test_dns_enum_imports():
    try:
        import dns_enum
    except ImportError as e:
        pytest.xfail(f"Required module for dns_enum not found: {e}. Install via: sudo apt install python3-dnspython")
