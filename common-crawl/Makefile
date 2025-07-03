CC = gcc
CFLAGS = -O3 -march=native -pipe
TARGET = cdx

# Include generated crawls makefile
include crawls.mk

# Override all target to build combined release
all: combined

# Build the C extractor
$(TARGET): cdx.c
	$(CC) $(CFLAGS) -o $@ $<

# Pattern rules for compression with deduplication
%.tsv.gz: %.tsv
	cat $< | LC_ALL=C sort -u | pigz -9 > $@.tmp && mv $@.tmp $@ && rm -f $<

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

# Generate expected merge output using naive Python implementation
test/expected_merge.txt: test/expected_domains.txt make_expected_merge.py
	@echo "Generating expected merge output..."
	@cat test/expected_domains.txt | python3 make_expected_merge.py > $@

test_merge: test/expected_merge.txt merge_domains.py
	@echo "Running merge tests..."
	@bash -c 'diff -u test/expected_merge.txt <(cat test/expected_domains.txt | python3 merge_domains.py test/expected_merge.txt && cat test/expected_merge.txt) && echo "Merge tests passed!" || { echo "Merge tests failed! See differences above."; exit 1; }'

test: test_cdx test_merge

.PHONY: all clean distclean test_cdx test_merge test