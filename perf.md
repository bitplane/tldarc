# Performance Comparison: CDX Domain Extraction

Testing with CC-MAIN-2008-2009 cdx-00000.gz (307MB compressed, 4.9M lines, 636K unique domains)

| Approach | Speed | Real Time | User Time | Sys Time | Output Lines | Notes |
|----------|-------|-----------|-----------|----------|--------------|-------|
| Original sed (regex) | ~0.65 MB/s | - | - | - | - | Complex regex with backreferences |
| Cut pipeline (9 stages) | 39.6 MB/s | 7.9s | 29.8s | 8.9s | 4.9M | 9 pipes: cut/tr chain |
| Cut + awk pipeline | 8.2 MB/s | 37.7s | 41.9s | 2.7s | 4.9M | Awk for final formatting |
| Optimized sed | 2.2 MB/s | 142s | 146.8s | 2.4s | 4.9M | Simpler regex, \L for lowercase |
| **C program (no dedup)** | 48.7 MB/s | 6.3s | 9.7s | 3.4s | 4.9M | Direct byte scanning |
| C + uniq | 49.4 MB/s | 6.2s | 10.3s | 3.7s | 2.6M | Adjacent dedup only |
| C + sort -u | 19.4 MB/s | 15.8s | 18.3s | 2.5s | 636K | Full deduplication |
| C + uniq + sort -u | 20.9 MB/s | 14.7s | 18.0s | 3.0s | 636K | Marginal improvement |
| **C + Python set** | 32.4 MB/s | 9.5s | 11.8s | 4.5s | 636K | Hash-based dedup |

## Analysis

- **C program eliminates extraction bottleneck** - 6.3s vs 7.9s for best shell solution
- **Python set dedup beats sort -u** - 9.5s vs 14.7s (35% faster)
- High duplicate rate: 4.9M lines → 636K unique (87% duplicates)
- `uniq` only removes 47% (adjacent duplicates), showing heavy interleaving
- Higher sys time with Python (4.5s) due to large buffer I/O, but still faster overall

## Final Pipeline Performance

- **Best configuration**: C extractor + Python set deduplication
- **Throughput**: 32.4 MB/s compressed data
- **Total time**: 9.5s per 307MB file
- **Bottleneck**: Now shifted to decompression (pigz/zstd ~30% faster than gzip)

## Recommendations

1. Use C extractor + Python set for single files
2. Process multiple files in parallel for gigabit connection utilization  
3. Consider bloom filter for even faster approximate deduplication
4. Final merge can use sort -u across all files