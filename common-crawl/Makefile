CC = gcc
CFLAGS = -O3 -march=native -pipe
TARGET = cdx

# Include generated crawls makefile
include crawls.mk

# Build the C extractor
$(TARGET): cdx.c
	$(CC) $(CFLAGS) -o $@ $<

# Pattern rules for compression
%.tsv.gz: %.tsv
	gzip -9 $<

# Add cdx dependency to all .tsv targets from crawls.mk
%.tsv: $(TARGET)

clean:
	rm -f $(TARGET) *.tsv *.tsv.gz

distclean: clean
	rm -f crawls.mk

.PHONY: all clean distclean