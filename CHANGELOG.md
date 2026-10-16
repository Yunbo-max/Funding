# Changelog

## 0.2.0 — 2026-10-16

- Studied [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) core architecture, command workflows, portal search adapters, ranking/state helpers, document rendering and layout, privacy security, outcomes and tests. Maintained attribution and independently authored source.
- Added eight command playbooks: setup, discover, rank, apply, outcome, add-source, expand, report/inbox. Added official-funder adapter contract and detailed comparative study.
- Added `pipeline.py` for private structured call intake, stable funder/program/round IDs, source sightings, bounded queues, conservative route-by-route ranking, explicit application stages and human-confirmed outcomes, and self-contained escaped HTML report.
- Added `verify_grant_pdf.py` for optional local PDF page count, readable text, required text and placeholder checks with explicit visual-review caveat.
- Added 18 pipeline tests and 4 PDF verification tests; **22/22 passed locally in isolated source tests**. Original 20 eligibility/writing tests remain present; they were not rerun in the isolated new-module checkout.
- No live portal scraper, background scheduler, application submission or institutional PI confirmation is claimed. No GitHub Actions/workflow files introduced.

## 0.1.0 — 2026-10-16

- CV-gated official funding research, eligibility rules and funder-shaped proposal-writing skill.
- Evidence and privacy contracts, local intake/shortlist/audit, and original 20-test baseline.
