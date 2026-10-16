# Changelog

## 0.3.0 — 2026-10-16

- Added **native Claude Code commands** `/setup`, `/search`, `/rank`, `/apply`, `/outcome`, and `/status` with a unified on-demand researcher application journey.
- Added `skills/funding-autopilot/scripts/workspace.py`: CLI onboarding from an uploaded CV, user-reviewed profile, safe incremental preference edits, UKRI RSS or AI-host sourced lead ingestion, exact round promotion, independent/new-PI route decisions, funder-specific local application folders, PI outreach scaffolds and receipt-backed tracking.
- Prevented planned doctoral submission/degree award dates from being misrepresented as completed milestones, including future actual dates.
- Repeated searches of already-verified calls avoid an extra `unverified` duplicate and trigger official round rechecks.
- Added call-specific ready/audit constraints. A structured draft is not treated as submitted; new PI or host approvals remain explicit.
- Added 14 new fictional-fixture user-workflow tests. All 14 passed in the isolated local test harness using **interface-equivalent test doubles** for the existing `funding.py` and `pipeline.py`; the old core regression suite and real external source integration were **not** rerun in that same harness. See [validation notes](docs/VALIDATION-0.3.md).
- No GitHub Actions, workflow runs, automatic mailing, unattended schedulers, real grant submissions or public CV files.

## 0.2.0 — 2026-10-16

- Studied [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) core architecture, command workflows, portal search adapters, ranking/state helpers, document rendering and layout, privacy security, outcomes and tests. Maintained attribution and independently authored source.
- Added eight command playbooks: setup, discover, rank, apply, outcome, add-source, expand, report/inbox. Added official-funder adapter contract and detailed comparative study.
- Added `pipeline.py` for private structured call intake, stable funder/program/round IDs, source sightings, bounded queues, conservative route-by-route ranking, explicit application stages and human-confirmed outcomes, and self-contained escaped HTML report.
- Added `verify_grant_pdf.py` for optional local PDF page count, readable text, required text and placeholder checks with explicit visual-review caveat.
- Added 18 pipeline tests, 4 PDF verification tests and 9 UKRI adapter tests; **31/31 passed locally in isolated source tests**. Original 20 eligibility/writing tests remain present; they were not rerun in the isolated new-module checkout.
- Added an official UKRI RSS discovery adapter, tested offline against synthetic XML. The actual public RSS address was confirmed through the official UKRI Funding Finder page, but live outbound fetching and parsing was not tested here. No exhaustive funding scraper, background scheduler, application submission or institutional PI confirmation is claimed. No GitHub Actions/workflow files introduced.

## 0.1.0 — 2026-10-16

- CV-gated official funding research, eligibility rules and funder-shaped proposal-writing skill.
- Evidence and privacy contracts, local intake/shortlist/audit, and original 20-test baseline.
