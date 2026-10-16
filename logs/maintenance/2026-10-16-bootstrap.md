# 2026-10-16 bootstrap and validation

Project: Funding Autopilot (public open-source skill)
Observed pre-log repository revision: `ead84f32201cb3d50acc29e5b8b5f551f552d568`
GitHub source commit tree: `5e379c4bd16de246bf208f7e6a5d3aaee652850f`

## Scope of work
- Created standard Agent Skills entry point, funder-source registry, CV privacy, eligibility, discovery and writing guides.
- Added explicit independent and new-PI/host pathways and separate thesis-submission vs degree-award checks.
- Added offline, standard-library CLI for CV intake, conservative route-based shortlisting, verified-call-specific proposal scaffold, and section/claim evidence audit.
- Added synthetic example only; no user CV, proposal, email, contact data or real funder decision recorded.

## Actually executed on local Python host
- Command: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`
- Result: **20 tests passed; exit code 0**.
- Actual smoke commands: `intake`, `shortlist`, `prepare` with private *fictional* CV and test call; exit code 0.
- Smoke outcome: unreviewed CV produced **conditional** for independent and new-PI paths, not a false eligible status; generated blank funder-shaped draft under ignored private path.
- Tests include source freshness, missing primary evidence, offset-aware timestamps, internal deadline, CV required, expected-vs-actual doctorate milestones, residence mismatch, PI confirmation, word limits, claim IDs, attachments and placeholders.

## Remote round-trip proof
- Local-tested `skills/funding-autopilot/scripts/funding.py` Git blob SHA: `eb3ff093f3ce485e8ed159a7e2a3617c5f73394f`; exact remote readback matched.
- Local-tested `tests/test_funding.py` Git blob SHA: `d073b3130bccaf614e57fba974421f1c3960e12a`; exact remote readback matched.
- `.github/workflows/` entries in published tree: **0**. No GitHub Actions, workflow run, workflow_dispatch or CI invocation was used.

## Not established by these checks
- No live AI-host end-to-end online search or proposal drafting trial has been performed.
- No real applicant eligibility, submitted grant, PI commitment, funder approval, or background scheduler has been verified.
- Official source registry comprises verified entry-point URLs, not curated active individual calls.
- PDF/DOCX optional parsers are supported in code, but this check's regression suite exercises TXT intake.

Next validation should use a user-authorized uploaded CV plus an officially retrieved current scheme, keeping all personal materials out of this public repository.
