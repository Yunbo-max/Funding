# /add-source — Create a verified funder search adapter

Read `../references/source-adapter-contract.md`. Given a funder portal URL:

1. Verify whether the site is official, public, current, and usable. Check terms, robots directives and any published API before generating a client. Do **not** bypass authentication, CAPTCHA, login walls, robots disallow rules, throttling or access-control restrictions.
2. Establish a narrow **search** operation (query, page, limit, jurisdiction, stage) and a **detail** operation (exact call ID or official URL). When no documented API/search is available, the adapter can be an **agent web-search specification**, not a fake working scraper.
3. Normalize results into the call contract: funder, official programme ID, round, title, verified-or-lead URL, source kind, opened/close dates if published, actual source timestamp and link to full official guidance; preserve absent fields as null.
4. Detect rate limits, outages, partial HTML/search results and contradictory call versions. Never interpret an error/403 as "zero open grants." Prefer host search fallback with an explicit unverified flag.
5. Provide versioned documentation, required environment variables (if any, never tokens embedded in URL/flags), a fictional fixture, unit tests for empty/invalid/duplicate/expired results, and a **live one-query test** when actual web/host permission exists.
6. Source connectors are pluggable, opt-in, and have no background schedules. Registration alone does not claim the adapter was tested or a funder allows scraping.

Outcome: source manifest plus a tested search/detail strategy, or a documented read-only manual/host-search fallback.
