# Changelog

## 0.4.0 — 2026-10-16

- Replaced all four previously dark/gradient AI-style diagrams with **original flat editorial SVG art** (warm ivory, forest green, brick red, serif headline typography and restrained graph-paper geometry). Illustrations remain editable and self-contained in the public repository.
- Translated the research-readiness headline into idiomatic English throughout the **public English README and hero**, removed Chinese navigation, and retired the separate Chinese translation to keep the project presentation English-only. The slogan is aspirational rather than a funding-success guarantee.
- Documented a reusable [visual identity](docs/ART-DIRECTION.md) and extended README regression tests to guard English text, SVG resource independence and removal of glow/gradient effects.


- Added sourced, balanced comparison of grant tools plus original twelve-month funding-readiness and five-proposal-type vector illustrations; updated bilingual motivational tagline without promising awards.
- Added /year-plan as a one-time Claude Code AI-host planning playbook using verified calls and private CV facts; does not activate background monitoring or add a Python scheduler.
- Added scheme-specific writing strategies for fellowships, PI-led research grants, consortia, innovation projects and past-impact awards, integrated into Prepare/Apply.

- Added `/match` (with `/rank` alias), a separate `/prepare` command and an explicit applicant-reviewed `prepare-complete` gate ahead of `/apply`.
- Expanded the private application state graph: selected → preparing → prepared → drafting; recorded funder-specific research strategy, section outlines, confirmed CV evidence facts and PI/Host/budget conditions.
- `/apply` now refuses to jump straight from matching to proposal drafting; a conditional host may support an exploratory concept but never final submission-ready approval.
- Added original vector GitHub hero and six-stage workflow illustrations, updated Skill/Claude commands and installation/English/Chinese documentation.
- Added regression cases targeting bypasses, unsupported evidence, missing outlines, plan confirmation, and new-PI preparation. **Full runtime test execution was not performed in this source update**; see `docs/VALIDATION-0.4.md`.


## 0.3.0 — 2026-10-16

- Added **native Claude Code commands** `/setup`, `/search`, `/rank`, `/apply`, `/outcome`, and `/status` with a unified on-demand researcher application journey.
- Added `skills/funding-autopilot/scripts/workspace.py`: CLI onboarding from an uploaded CV, user-reviewed profile, safe incremental preference edits, UKRI RSS or AI-host sourced lead ingestion, exact round promotion, independent/new-PI route decisions, funder-specific local application folders, PI outreach scaffolds and receipt-backed tracking.
- Persisted CV-grounded publications, projects, awards, education and research claims as private, source-located facts for user review. Resolved fact IDs are deduplicated and conflicts flagged instead of silently overwritten.
- Prevented planned doctoral submission/degree award dates from being misrepresented as completed milestones, including future actual dates.
- Repeated searches of already-verified calls avoid an extra `unverified` duplicate and trigger official round rechecks.
- Added call-specific ready/audit constraints. A structured draft is not treated as submitted; new PI or host approvals remain explicit.
- Added 16 new fictional-fixture user-workflow tests. All 16 passed in the isolated local test harness using **interface-equivalent test doubles** for the existing `funding.py` and `pipeline.py`; the old core regression suite and real external source integration were **not** rerun in that same harness. See [validation notes](docs/VALIDATION-0.3.md).
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
