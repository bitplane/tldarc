CC = gcc
CFLAGS = -O3 -march=native -pipe
TARGET = cdx

# Include generated crawls makefile
include crawls.mk

# Build the C extractor
$(TARGET): cdx.c
	$(CC) $(CFLAGS) -o $@ $<

# Pattern rules for compression with deduplication
%.tsv.gz: %.tsv
	cat $< | sort -u | pigz -9 > $@

# Add cdx dependency to all .tsv targets from crawls.mk
%.tsv: $(TARGET)

# Mark pattern for TSV files as intermediate - they'll be cleaned up after compression
.INTERMEDIATE: %.tsv

clean:
	rm -f $(TARGET) *.tsv *.tsv.gz

distclean: clean
	rm -f crawls.mk

test_cdx: $(TARGET)
	@echo "Running cdx tests..."
	@bash -c 'diff -u test/expected_domains.txt <(cat test/test_domains.txt | ./cdx) && echo "All tests passed!" || { echo "Tests failed! See differences above."; exit 1; }'

test: test_cdx

.PHONY: all clean distclean test_cdx test