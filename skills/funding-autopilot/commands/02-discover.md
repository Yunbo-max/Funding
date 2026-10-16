# /discover — Multi-source opportunity discovery

Input: uploaded-CV-grounded profile, constraints and search horizon.

1. Generate distinct search families (research terms, foundational methods, interdisciplinary applications, individual fellowships, externally hosted fellowship, new PI grants, salary-funded postdocs). Search broadly across the requested geographic regions; do not anchor to the current supervisor.
2. Use web/search tools and official-funder portals. Source adapters must obey `../references/source-adapter-contract.md`. Search result snippets and aggregators are **leads only**. Deduplicate by funder + programme ID + round; preserve all observed URLs, feed source and time.
3. Call `pipeline.py --state private/ledger.json ingest --input private/new-calls.json` after an agent writes a candidate list. The helper does not itself search or verify websites.
4. For up to N new leads, retrieve the **full active round** official page and all accessible linked guidance, not just a title and deadline. Extract eligibility, source section/paragraph, required documents, host role, allowable salary, institutional approval, review criteria, actual submission portal and time zone. Record a UTC checked-at timestamp and the precise source. If a page is blocked, report it, do not fabricate contents.
5. Find receiving institution/department/internal dates independently and mark `unknown` if not published; changing host restarts that check. Do not assume a grant is active from last year's page.
6. Keep source access issues separate from scientifically irrelevant calls and actual expired calls. Stale/blocked sources remain unverified, not "no funding found".

Outcome: an explicit table of discovered/verified/unverified leads with the source and next verification task. Run `rank` only after this breadth pass.
