#!/bin/bash

INPUT="$1"
OUTPUT="$2"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Usage: $0 <input.tsv> <output.tsv>"
  exit 1
fi

# Compare only YYYYMM of first and last seen
awk -F'\t' 'substr($2, 1, 6) != substr($3, 1, 6)' "$INPUT" > "$OUTPUT"

# Report stats
echo "Original lines: $(wc -l < "$INPUT")"
echo "Filtered lines: $(wc -l < "$OUTPUT")"
echo "Filtered size: $(du -h "$OUTPUT" | cut -f1)"
