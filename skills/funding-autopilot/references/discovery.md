# Funding discovery and primary-source research

## Worldwide scope and source-coverage accounting

The user selects a country, a set of regions, or "worldwide". **Do not restrict the search to their present institution or country.** A global search requires actual host-side browsing/search across the chosen regions; the repository does not bundle a global crawl. The built-in UKRI RSS feed is one recent-items connector only, not the engine for searches in Canada, Europe, America, Asia, Africa, Latin America or Oceania.

Start with the [official source registry](../assets/source-registry.json): public UK, EU, US, Canada, Australia, Germany, Singapore, Japan, Brazil, South Africa and New Zealand research funding portals, where relevant, then extend to host institutions and funder-specific webpages. The registry contains **portals, not live open opportunities or applicant approvals**. Query across multiple source families and local languages when necessary.

For each geographic lane, record `region | official portals queried | date searched | actual round documents opened | access failures | lead counts | still unsearched`. A query result count is not coverage completeness. If the host cannot read local legal/degree/host requirements, call the case `unverified`; do not silently recommend it as eligible.

International mobility needs two independent checks: (a) is the **person and role** eligible, by application/start date and citizenship/residency conditions where applicable; (b) is the **receiving institution** eligible and willing to be PI/host, and what is its earlier internal deadline? A grant available in a country may be institution-only or restricted to specific nationalities. Distinguish a salary-funded fellowship from a PI's project grant.

## Search strategy: breadth, then primary source

Derive 3–6 keyword families from the CV: exact research subfields, broader concepts, methods, societal applications, researcher career stage and role/host alternatives. For each relevant jurisdiction and funder, search official pages using combinations of topical and eligibility terms, e.g. "postdoctoral fellowship", "doctoral thesis submitted", "individual grant", "early career", "open source", "new host institution", "research software", "AI agents". Vary families to avoid overfitting to a single keyword.

Start from the official portals in [source-registry.json](../assets/source-registry.json); include local departmental funding announcements supplied by the user. For university/internal calls, verify with the receiving department, which may differ from the applicant's current research group. Aggregators, mailing lists, blogs and search snippets are discovery leads, not evidence of eligibility or deadlines.

For the user seeking a new PI, deliberately search three parallel routes:
1. **Own project/independent applicant:** fellowship, individual grant, independent award.
2. **New-PI or host-backed grant:** new lead based in a different group, budget line for researcher's salary only if permitted; the PI must meet its own rules.
3. **New institution employment/fellowship:** externally hosted fellowships, advertised postdoctoral opportunities with separate selection.

Differentiate grants, jobs, awards/prizes and contracts. A prize may help visibility but does not establish future employment; an institutional grant may not pay the applicant's salary.

## Candidate record and provenance

For each call capture the exact round identifier, official URL, issuing body, funding modality, likely role/route, opening/current status, official guidance version, downloaded PDF/link and whether it can be reached, official deadline and timezone, internal deadline/approval, eligibility and post-award conditions, required annexes, limits and budget/salary conditions. Keep field-level citations: exact page/section/paragraph, checked-at UTC and source kind.

Use multiple independent searches to look for amendments/extensions. Prefer the current official round page over past cycle announcements. Compare call guidelines, FAQ and institutional policy; record and flag conflicts explicitly. Never silently choose the more convenient deadline. Use "unknown" if a field could not be checked.

## Quality gates

- A search result without a current specific official call page remains **discovered/unverified**.
- Record both funder deadlines and relevant internal dates; if host changes, recheck its internal deadline.
- Treat "rolling" separately from "no published deadline"; no guarantee that the round is currently accepting.
- Date fields must distinguish announcement publication from call close; store timezone and ideally UTC offset.
- Similar titles across cycles are not duplicates; de-duplicate by funder + call ID + round.
- If a public source conflicts with an institutional email, flag both with source/date; ask appropriate grants office for clarification rather than invent a reconciliation.

## Evidence freshness

Check a call on the day of a recommendation where possible. A locally structured helper uses a conservative default 30-day staleness threshold; this is **not** the funder's rule. Even a younger cached page might have been amended; for imminent deadlines, re-open the original page.

The search host's inability to browse means it may supply official *entry points*, not claim verified live calls.
