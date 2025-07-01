#!/bin/bash

# Extract domains from Common Crawl CDX format (reads from stdin)
extract_cdx_domains() {
    # Fast pipeline using only cut and tr
    cut -d ' ' -f 2- | \
    cut -c 1-8,15- | \
    cut -d ';' -f1 | \
    tr " " "," | \
    cut -d ',' -f 1,3 | \
    tr ':/' ',' | \
    cut -d ',' -f1,6 | \
    tr ',' '\t' | \
    tr '[:upper:]' '[:lower:]'
}

# Process URL list from stdin, stream each CDX file
process_url_list() {
    local base_url="https://data.commoncrawl.org/"
    while read -r path; do
        if [[ "$path" == *cdx-*.gz ]]; then
            echo "Processing $path..." >&2
            curl -s "${base_url}${path}" | pv | zstd -dc | extract_cdx_domains
        fi
    done
}