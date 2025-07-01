#!/bin/bash

# Extract domains from Common Crawl CDX format (reads from stdin)
extract_cdx_domains() {
    # Use compiled C program for maximum speed
    ./extract_cdx
}

# Process URL list from stdin, stream each CDX file
process_url_list() {
    local base_url="https://data.commoncrawl.org/"
    while read -r path; do
        if [[ "$path" == *cdx-*.gz ]]; then
            echo "Processing $path..." >&2
            curl -s "${base_url}${path}" | pigz -dc | extract_cdx_domains | python3 -c "import sys; sys.stdout.write('\\n'.join(set(sys.stdin.read().strip().split('\\n')))+'\\n')"
        fi
    done
}

