# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tldarc is a domain name collection and analysis project that extracts domain names from Common Crawl data to build a comprehensive, freely available domain list without relying on zone files from registrars.

## Common Development Commands

### Setup and Build
```bash
# Initial setup - checks dependencies and generates build files
./configure

# Build the C domain extractor
cd common-crawl && make

# Run tests to verify the extractor works correctly
make test_cdx
```

### Processing Common Crawl Data
```bash
cd common-crawl

# Process the most recent crawl
make latest

# Process a specific crawl
make CC-MAIN-2025-26.tsv.gz

# Process all crawls (warning: this downloads and processes TBs of data)
make all

# View statistics on processed domains
make stats
```

### Clean Up
```bash
# Remove compiled binaries and generated data files
make clean

# Also remove generated crawls.mk
make distclean
```

## Architecture Overview

### Data Pipeline
1. **Configure Script** (`./configure`) - Checks for required dependencies (curl, aria2c, pigz, python3, parallel, make, gcc) and generates `crawls.mk` by fetching the Common Crawl index
2. **Makefile System** - Two-part build system:
   - `Makefile`: Main build configuration, compiles the C extractor
   - `crawls.mk`: Generated targets for each Common Crawl collection
3. **crawl.sh** - Downloads Common Crawl CDX files in parallel and pipes through the extractor
4. **cdx.c** - High-performance C program that:
   - Parses Common Crawl CDX format (space-delimited)
   - Extracts domain names from URLs in column 3
   - Filters out IP addresses and numeric-only domains
   - Normalizes domains to lowercase
   - Outputs TSV format: `timestamp\tdomain`

### Key Design Decisions
- **Performance Focus**: C extractor for maximum speed when processing TB-scale data
- **Parallel Processing**: Uses GNU parallel for concurrent CDX file processing
- **Compression**: All output files are compressed with pigz -9 to save space
- **Incremental Processing**: Each crawl can be processed independently
- **Deduplication**: Happens at the crawl.sh level using Python set operations

### Testing
The project includes a simple but effective test harness:
- Test input: `test/test_domains.txt` - Contains various URL formats to test edge cases
- Expected output: `test/expected_domains.txt` - Expected domain extraction results
- Run with: `make test_cdx`

## Future Roadmap (from README.md)
- Feed domain data into a database
- Get TLD data for filtering
- Stream certificate transparency data
- Publish raw data files to HuggingFace, GitHub, Internet Archive
- Create MCP server for domain queries