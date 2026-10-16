# Funding discovery and primary-source research

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
