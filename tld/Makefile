# TLD validation and domain filtering

# Download raw TLD list
tlds.txt:
	@echo "Downloading TLD list..."
	@curl -s "https://data.iana.org/TLD/tlds-alpha-by-domain.txt" | \
	grep -v '^#' | \
	tr '[:upper:]' '[:lower:]' > $@

# Generate regex pattern from TLD list
tlds.regex.txt: tlds.txt
	@echo "Generating TLD regex pattern..."
	@cat tlds.txt | \
	sed 's/^/\\./' | \
	sed 's/$$/$$/' | \
	tr '\n' '|' | \
	sed 's/|$$//' > $@

clean:
	rm -f tlds.txt tlds.regex.txt

.PHONY: clean