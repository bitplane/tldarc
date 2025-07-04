#!/usr/bin/env python3

import sys
import codecs

def convert_punycode_to_utf8(line):
    """Convert punycode TLD to UTF-8 if it starts with xn--"""
    tld = line.strip()
    if tld.startswith('xn--'):
        try:
            # Extract the punycode part (after xn--)
            punycode_part = tld[4:]  # Remove 'xn--' prefix
            # Decode punycode to Unicode
            utf8_tld = codecs.decode(punycode_part, 'punycode').encode('utf-8').decode('utf-8')
            return utf8_tld
        except Exception:
            # If conversion fails, return original
            return tld
    return tld

def main():
    for line in sys.stdin:
        utf8_tld = convert_punycode_to_utf8(line)
        print(utf8_tld)

if __name__ == '__main__':
    main()