#!/bin/bash

# Filter out domains with valid TLDs from data files
# Usage: ./bad.sh *.gz

# Get the valid TLD pattern
get_valid_tlds() {
    curl -s "https://data.iana.org/TLD/tlds-alpha-by-domain.txt" | \
    grep -v '^#' | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/^/\\./' | \
    sed 's/$/$/' | \
    tr '\n' '|' | \
    sed 's/|$//'
}

# Cache the TLD pattern to avoid repeated downloads
if [ ! -f .tld_pattern ]; then
    echo "Downloading and caching TLD pattern..." >&2
    get_valid_tlds > .tld_pattern
fi

VALID_TLD_PATTERN=$(cat .tld_pattern)

# Filter out domains that end with valid TLDs
if [ $# -eq 0 ]; then
    grep -vE "$VALID_TLD_PATTERN"
else
    zcat "$@" | grep -vE "$VALID_TLD_PATTERN"
fi