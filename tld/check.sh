#!/bin/bash

# Filter out domains with invalid TLDs from data files
# Usage: ./check.sh [files...]
# Or: cat file | ./check.sh

# Path to the TLD regex pattern file
REGEX_FILE="tlds.regex.txt"

# Build the regex pattern if it doesn't exist
if [ ! -f "$REGEX_FILE" ]; then
    echo "Building TLD regex pattern..." >&2
    make tlds.regex.txt
fi

# Check if the regex file exists after build attempt
if [ ! -f "$REGEX_FILE" ]; then
    echo "Error: Could not create TLD regex pattern file" >&2
    exit 1
fi

VALID_TLD_PATTERN=$(cat "$REGEX_FILE")

# Filter out domains that end with valid TLDs
if [ $# -eq 0 ]; then
    # Read from stdin, extract just the domain part, then filter
    cut -f1 | grep -vE "$VALID_TLD_PATTERN"
else
    # Process files, extract domain part, then filter
    zcat "$@" | cut -f1 | grep -vE "$VALID_TLD_PATTERN"
fi