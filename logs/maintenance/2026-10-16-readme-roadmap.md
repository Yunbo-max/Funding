# Funding Autopilot: global README, comparison and annual planning

Date: 2026-10-16
Parent source revision verified before this log: `7301c53535464685f05b1642b17c9ddfcc75a486`

## Published

- GitHub README starts with the owner's exact Chinese readiness motto, a concise English tagline, and a disclaimer that grant success is not guaranteed.
- Main page now emphasizes worldwide **agent-assisted** funding research and transparently states that only UKRI recent RSS is a bundled standalone search connector.
- A balanced comparison table references PaperBreak, GrantWell, grant-finder and Grantable, including their actual publicly documented strengths and the different built-in search maturity.
- Original vector graphics: `assets/yearly-roadmap.svg` (12 relative months of overlapping funding readiness) and `assets/proposal-strategies.svg` (five funding types); original `assets/hero.svg` and `assets/workflow.svg` remain. The workflow SVG's unescaped ampersands were repaired.
- `docs/PROJECT-COMPARISON.md` grounds the comparison in relevant product sites and GitHub READMEs; `docs/PROPOSAL-STRATEGIES.md` explains how distinct grant types need different proposal arguments.
- `/year-plan` agent command/playbook documents generating a personal, source-linked, 12-month `private/annual-plan.md` from verified opportunities without inventing dates or starting a scheduler.
- Updated main Agent Skill, CLAUDE guidance, proposal preparation, English and Chinese docs, and changelog.
- Added `tests/test_readme_assets.py` to run Python's XML parser and README linkage assertions on future local validation.

## Actually verified in this session

Using authenticated direct GitHub fetches plus deterministic in-process structural checks:
- All four published SVG assets have balanced XML-like tags, SVG closing tags and no detected raw unescaped ampersands.
- All relative README Markdown links and the hero image source resolve to paths in the published repository tree.
- README contains the motto, comparison, yearly roadmap, scheme writing strategies, explicit Input → Output sample and non-first-mover disclosure.
- Repository contains **no `.github/workflows/` files**. No GitHub Actions/workflow runs/dispatches were invoked.
- The authorized `main` branch was updated with guarded direct Git commits and file readback.

## Not established

- No full Python test suite, browser/PDF visual render or live grant search was executed as part of this documentation update. In particular, the newly added Python graphics test is present but **has not yet been executed here**.
- The annual plan command is an **AI host playbook**, not an installed Python automatic scheduler or guaranteed repeated check.
- No new global source adapters were implemented, and no real funding application, researcher employment, PI commitment or award was asserted.
- The header is an aspirational slogan, not a funding-success guarantee or a statement that no researcher faces real structural barriers.
