# Persistent private pipeline (v0.2)

Like the stateful search → rank → apply → outcome progression in the reference job-search framework, Funding stores a **candidate call ledger**, but application stage and eligibility status remain separate.

## Call identity and records

The stable key is `sha256(normalized funder + official programme identifier + round)[:20]` prefixed `call-`. Never derive a key from mutable programme title, search query or time of discovery. Distinct funding rounds always receive separate keys. A source's seen URL and checked timestamp are stored; repeated discovery adds provenance but **cannot silently overwrite an existing verified call**. Refreshed call rules require an explicit human/agent re-verification of the official source.

`private/ledger.json` holds a `calls` dictionary indexed by that key. Each record contains `call` (full agent-populated source data), `sources`, `first_seen`, `last_seen`, `stage`, `route`, `evaluations`, `history`.

`status` in an `evaluation` is `eligible`, `conditional`, `unverified`, `ineligible`, `expired`. The application's independent `stage` is `discovered`, `shortlisted`, `selected`, `drafting`, `draft_ready`, `submitted`, `under_review`, `awarded`, `rejected`, `withdrawn`, or `archived`. Never write a status phrase into the other field.

## Commands

```bash
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json ingest --input private/discovered-calls.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json batch --limit 10
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json rank --profile private/profile.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json advance --key call-EXAMPLE --to shortlisted
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json report --out private/funding-report.html
```

Selection of a call and route must be backed by eligibility evidence, even if conditional at the concept stage. No draft is ready until the selected route is eligible. Submitted/awarded/rejected/withdrawn states require explicit confirmation and evidence reference, which the tool records in a history item. Recheck official-source freshness/deadlines before moving to ready/submitted.

The ledger is written atomically, and a `batch` prints only compact rows and a deferred count. Deferred opportunities remain eligible for a future batch. Terminal outcomes are kept for analysis rather than deleted. Re-opening archived leads is explicit.

Keep the ledger and generated HTML under a resolved `private/` directory, never inside the public source paths. The HTML report escapes third-party strings and uses no network resources. Underlying JSON may contain sensitive call and role information: never commit or publish it without explicit consent.

## Authority/limits

The helper validates a subset of the encoded constraints but cannot certify official guidance was read correctly; only a real evidence-grounded host review and the institution may establish an applicant's actual eligibility. There is no automatic contact, submission, mail sync, scheduling or live browsing in the CLI. Use the appropriate host tool only on explicit authorization.
