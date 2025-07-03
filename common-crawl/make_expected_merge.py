#!/usr/bin/env python3
"""
Simple reference implementation: load all data into RAM, merge, sort, output.
Use this to generate the correct expected_merge.txt file.
"""

import sys
from collections import defaultdict

def main():
    # Dictionary to accumulate: domain -> [list of timestamps]
    domains = defaultdict(list)
    
    # Read all input
    for line in sys.stdin:
        try:
            parts = line.strip().split('\t')
            if len(parts) != 2:
                continue
            domain, timestamp = parts
            domains[domain].append(timestamp)
        except:
            continue
    
    # Process each domain: find min/max timestamps
    results = []
    for domain, timestamps in domains.items():
        first = min(timestamps)
        last = max(timestamps)
        results.append((domain, first, last))
    
    # Sort by domain name
    results.sort()
    
    # Output
    for domain, first, last in results:
        print(f"{domain}\t{first}\t{last}")

if __name__ == "__main__":
    main()