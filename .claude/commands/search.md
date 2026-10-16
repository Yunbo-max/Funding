# /search — Find real research funding, not just generic matching words

Read `skills/funding-autopilot/commands/02-discover.md`, `references/discovery.md` and `references/source-adapter-contract.md`; use `$ARGUMENTS` as the focus.

1. Require the CV-backed setup profile (run `/setup` first if missing). Load user preferences from `private/profile.json`, not from public repository files. A previously approved profile should not be re-uploaded each time.
2. Derive separate query sets for the person's research and career stage: own-name fellowships, early-career research grants, **new PI/host-led** schemes, postdoc salary funding, collaborative calls and research prizes where relevant.
3. For UKRI's public recent-items feed, run `python3 skills/funding-autopilot/scripts/workspace.py search --query "<comma-separated terms>"` if the runtime can use HTTPS. This is a **bounded recent RSS feed**, not an exhaustive catalogue.
4. For European Commission F&T, ARIA, charitable foundations, private funders and university-specific notices, use the host's actual current web/browser/search tools, then save a JSON array of `{id, funder, round, title, official_url, discovered_via}` leads to `private/discovered-calls.json` and import using `workspace.py search --input-file private/discovered-calls.json`. `round=unverified` is allowed for leads and must later be replaced from official guidance.
5. Use `pipeline.py --state private/ledger.json batch --limit 10` to work on a bounded, deduplicated set. Open the **exact official current-round** page and linked PDF/FAQ, read applicant/host eligibility, mandatory forms, salary rules, costs, and funder deadline. Search receiving institution internal deadline separately. For each source-backed candidate, create `private/verified-call-<safe-identifier>.json` with exact clauses, checked-at, round and source locators (see `references/records.md`).
6. Apply `workspace.py verify --key <lead-key> --call-file private/verified-call.json`. The call ID/funder and original official host must match. A structured record is not proof that the human/agent read correct funder rules: recheck original source before recommendations.
7. Display strong leads and disqualified/unknown routes separately. Record dead pages and access failure as **unknown**, not `closed`. Never fabricate an official call or eligibility exception.

End by offering `/rank`, not by declaring that RSS search itself found confirmed open eligibility. Never push the private lead JSON to this public repository.
