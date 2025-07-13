# tldarc

Let's make a list of domains, so we don't have to go cap in hand to registrars
for zone files, sign agreements and pay them money when we don't even care about
most of them anyway and don't want to agree to keep things secret.

Then make an MCP server that knows a bit about domain names (existence, semantic
search, first seen, last seen).

## Use cases?

* local version of namechecker.vercel.app using MCP
* scraping and wayback dive starting points
* actually having a free public list that can be searched locally without huge
  licensing fees.

## Current plan

- [ ] Feed seen and domain data into a database
- [x] Download commoncrawl indexes and extract domain names
  - takes about ~~2.5~~ 8 days on my 1gbps connection, 35GB of output data,
    10TB of bandwidth, 50% of my 16 CPU cores due to fast C extraction.
- [x] TLD validation and domain filtering
  - `tld/` directory contains tools to download IANA TLD list and generate regex patterns
  - Can filter domains with invalid TLDs from collected data
- [ ] Stream in certificate transparency data
  - [ ] Leave it running, publish periodically

### Publishing

- [x] Get DOI from Zenodo (concept DOI for project, version DOIs for releases)
- [x] Initial release: Historical Common Crawl data (2008-2025)
- [ ] Distribute to multiple platforms:
  - [x] Zenodo, and get a DOI
  - [ ] Internet Archive (primary long-term archive)
    - [x] Add to rip's upload queue
  - [ ] HuggingFace Datasets (ML/API access)
  - [ ] GitHub Releases (archive.org torrent, URL)

## Data

The data can be downloaded [here](https://zenodo.org/records/15872040).

### Citing

Due to the license choice, citation is unnecessary. It's still nice though,
and I got a DOI and everything.

```text
Gareth, D. (2025). Common Crawl Domain Names (1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.15872040
```

