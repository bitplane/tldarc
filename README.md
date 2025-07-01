# tldarc

Let's make a list of domains, so we don't have to go cap in hand to registrars
for zone files, sign agreements and pay themmoney when we don't even care about
most of them anyway and don't want to agree to keep things secret.

## Data source ideas

* Some registrars publish zone files. Need a free account for most of them
  though. [research project](https://chatgpt.com/s/dr_686356043c1481918e04465053884ea9)
  and [github repo](https://github.com/jschauma/tld-zoneinfo) about getting
  access.
* Certificate Transparency lists have lots of domains in them.
* Does Mozilla publish their DNS over HTTPS query lists at all? They would be
  really useful.
* Are there data leaks out there?
* web.archive.org API queries, querying monthly or daily would be a decent way
  to get a lot of bulk data. Can we do wildcard monthly queries? can we get
  data dumps?
* usenet archives for earlier URLs
* Links found in Reddit data dumps
* Links found in basically any large machine learning and other data sources,
  like the pile, or stuff on The Eye (join their discord and ask)
* /r/datahoarder and chums too! They have
* links in Wikipedia database dumps, including talk pages. The time at which
  they were added ought to be a confirmation that they were live at the time.
  Might be tedious but pretty sure I have a wikipedia dumper somewhere and php
  scripts to parse the metadata.
* Get lists from web.archive.org via the API. If we can get monthly dumps from
  the start of the archive, that will give good data.
* There are some old Twitter firehose dumps out there, for domain at date info.
* Stack Overflow articles contain links, their data is dumped and timestamped.
* Tag with "date seen" and "seen by source" lists, maybe infer it? Then adding
  more data sources builds a richer and richer set of information.
* Maybe generic forum extractors to get domain at time by looking for links
* Write a fast C program that extracts domains from text in stdin, and pump into
  it.

## Thoughts on gTLDs

* Need to start with a gTLD list, because they vary in sizes.to.the.gtld
* Not sure if gTLDs have an end date, but they do have a start date. Have any
  gTLDs been removed due to war or whatever?
* Have these changed over time? Are subdomains flexible too? Like I know we
  have "police.uk" now, which we never used to have. Dunno if we can query
  `*.uk.`, but pretty sure we can't query `*.co.uk` and don't know if this will
  work across all domains.
* There may be a way to get these automatically, or might not. We might need
  to just grab all subdomains from various sources and sort them by reverse
  sort order, then infer which ones are orgs and which ones are held by nation
  states.

## CLAUDE

Help me out here. Discuss the above and we can work together on a plan. Let's
not steam ahead into solutionizing before we have a modular system worked out.


