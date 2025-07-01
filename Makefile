CC = gcc
CFLAGS = -O3 -march=native -pipe
TARGET = extract_cdx

# Include generated crawls makefile
include crawls.mk

# Build the C extractor
$(TARGET): extract_cdx.c
	$(CC) $(CFLAGS) -o $@ $<

# Add extract_cdx dependency to all .tsv targets from crawls.mk
%.tsv: $(TARGET)

clean:
	rm -f $(TARGET) *.tsv *.tsv.gz

distclean: clean
	rm -f crawls.mk

.PHONY: all clean distclean