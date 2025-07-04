# TLD validation and domain filtering

# Download raw TLD list
tlds.txt:
	@echo "Downloading TLD list..."
	@curl -s "https://data.iana.org/TLD/tlds-alpha-by-domain.txt" | \
	grep -v '^#' | \
	tr '[:upper:]' '[:lower:]' > $@

# Convert punycode TLDs to UTF-8
tlds.utf8.txt: tlds.txt
	@echo "Converting TLDs to UTF-8..."
	@cat tlds.txt | python3 convert_utf8.py > $@

# Generate regex pattern from UTF-8 TLD list
tlds.regex.txt: tlds.utf8.txt
	@echo "Generating TLD regex pattern..."
	@cat tlds.utf8.txt | \
	sed 's/^/\\./' | \
	sed 's/$$/$$/' | \
	tr '\n' '|' | \
	sed 's/|$$//' > $@

clean:
	rm -f tlds.txt tlds.utf8.txt tlds.regex.txt

.PHONY: clean