#!/bin/bash

# Extract domains from Common Crawl CDX format (reads from stdin)
extract_cdx_domains() {
    # Use compiled C program for maximum speed
    ./cdx
}

# Download and filter CDX paths file
get_cdx_paths() {
    local paths_url="$1"
    curl -s "$paths_url" | zcat | grep 'cdx-.*\.gz$'
}

# Process single CDX file with aria2c multithreaded download
process_single_cdx() {
    local base_url="https://data.commoncrawl.org/"
    local path="$1"
    echo "Processing $path..." >&2
    
    curl -s "${base_url}${path}" | \
        pigz -dc | \
        extract_cdx_domains | \
        python3 -c "import sys; sys.stdout.write('\\n'.join(set(sys.stdin.read().strip().split('\\n')))+'\\n')"
}

# Export for GNU parallel
export -f extract_cdx_domains process_single_cdx

# Main script: extract domains from a paths file URL
extract_domains() {
    local paths_url="$1"
    local jobs="${2:-4}"  # Default 4 parallel jobs
    
    get_cdx_paths "$paths_url" | parallel -j "$jobs" process_single_cdx
}

# If run directly, process paths URL from command line
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ $# -lt 1 ]]; then
        echo "Usage: $0 <paths_url> [parallel_jobs]" >&2
        echo "Example: $0 'https://data.commoncrawl.org/cc-index/collections/CC-MAIN-2024-10/indexes.paths.gz' 4" >&2
        exit 1
    fi
    
    extract_domains "$@"
fi

