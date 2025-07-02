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
- [ ] Stream in certificate transparency data
  - [ ] Leave it running, publish periodically
- [ ] Publish raw data files
  - [ ] IA and link to it
