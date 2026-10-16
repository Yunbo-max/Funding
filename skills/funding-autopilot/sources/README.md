# Funding source adapters

A search adapter implements only a **lead collection** pathway, not a grant eligibility engine. All results must be checked against the actual official current-round call and host-office rules before recommending application.

## UKRI official RSS adapter

UKRI Funding Finder publicly links to `https://www.ukri.org/opportunity/feed/` from the [official opportunity listing](https://www.ukri.org/opportunity/). The bundled Python stdlib adapter uses the feed, does not bypass login/robots/captcha, and emits conservative **unverified leads**.

```bash
python3 skills/funding-autopilot/sources/ukri_rss.py search --query "AI" --limit 20
python3 skills/funding-autopilot/sources/ukri_rss.py detail "https://www.ukri.org/opportunity/REPLACE-WITH-REAL-CALL-URL/"
```

Without `--xml-file` or `--html-file`, these commands require actual outbound HTTPS access from the host. Tested functionality: synthetic RSS parsing and safe normalization, query filtering, duplicate handling, official-host allowlist, hard rejection of redirects to external hosts, and HTML text extraction. **Not tested in a live outbound HTTPS session** due to the present CPU host's restricted network access. UKRI may change feed structure/availability, requiring repair. `/detail` returns extractable text marked `retrieved_unverified`, not funder-approved or complete eligibility rules.

IMPORTANT: the RSS feed is a **recent-items feed**, not an exhaustive funding database; filtering `--query` only searches items the feed returned. For comprehensive discovery, pair it with the host's search of [UKRI Funding Finder](https://www.ukri.org/opportunity/) and use independent source verification. The discovered row uses a provisional `round: "unverified"`; replace it with the exact round/ID after reading the guidance, reconciling the ledger identity instead of silently merging different rounds.

## Other platforms

The [European Commission Funding & Tenders Portal APIs](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/support/apis) document a public REST search API. A live EU adapter has **not** been implemented or tested. Additional funders can be added under `sources/` using [the adapter contract](../references/source-adapter-contract.md) and the [add-source playbook](../commands/06-add-source.md); tests must check valid empty responses separately from errors and enforce a real official guidance step.

All adapters produce public call metadata only; they do not receive or transmit CVs or applicant profiles.
