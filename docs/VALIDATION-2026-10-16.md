# Funding Autopilot 0.2 — development validation

Date: 2026-10-16. All example calls, profiles and receipts used below are fictional. No private applicant documents were committed.

## Tested locally (actual host execution)

Command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q` on an isolated workspace containing **new v0.2 modules** and their tests.

Observed result after UKRI module: `Ran 31 tests`, `OK`, exit code 0. Earlier, before the adapter, 22 tests passed. This covers:
- stable round-aware IDs, dedup across discovery sources, provenance preservation and bounded batches;
- mandatory CV hash, role-specific hard checks, user-confirmed status transitions and receipts;
- refusal to treat conditional/old calls as submission ready;
- fail-closed private output paths, path traversal and HTML escaping;
- JSON state round-trip/atomic write, actual CLI invocation and offline report;
- PDF page cap, extractable text, unresolved placeholders and visual-review disclaimer;
- UKRI RSS XML, malformed/empty feed, official domain allowlist, duplicate normalization, HTML extraction, query filtering and external redirect rejection.

The `rank` integration exercised `funding.py` via an intentionally limited test double for its rule interface. The actual `funding.py` has its **separate 20-test historical test suite** from 0.1, and was not re-run end-to-end as part of these 31. Therefore, **do not report '51 tests passed in a single run'**.

## GitHub readback

After publication, exact Git blobs were read back and compared against the local tested files (SHA-1 Git blob identifiers):
- `scripts/pipeline.py`: `a84e1c408bde7cb1ec58d61f1f31517cfb6956fa`
- `tests/test_pipeline.py`: `af1e994579d1fe0c6d9edc90e9f5c6a253275347`
- `scripts/verify_grant_pdf.py`: `7bdf471c5f367d976246fb9c9762dc602d9c38ae`
- `tests/test_verify_grant_pdf.py`: `8ac760f8c9fe3dfa862c1b55d2329e2de81c59d3`

The repository tree showed zero entries under `.github/workflows/`. GitHub was used for source reads, guarded direct commits and verification only, without Actions, workflow dispatches or workflow runs.

## Still unverified

- The UKRI RSS adapter has an offline-tested implementation, but live outbound fetch and parse were **not verified** on this restricted host. No other real source adapter was tested.
- No CV-upload-to-real-call end-to-end trial, grant application form rendering or PDF visual audit against a live scheme has been run.
- No actual user authorization was collected for sending correspondence or submitting grants. No external grants were applied to.
- Optional mailbox classification is a command specification, not an installed connector automation.
