CC = gcc
CFLAGS = -O3 -march=native -pipe
TARGET = extract_cdx

all: $(TARGET)

$(TARGET): extract_cdx.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean