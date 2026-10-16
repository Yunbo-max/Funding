# Design study: MadsLorentzen/ai-job-search

Reviewed: 2026-10-16. Reference repository: https://github.com/MadsLorentzen/ai-job-search (master at `407dc34a2c4951e4ea3b047eaccdf2e4081a139a`). Original author: Mads Lorentzen. Original repository license: MIT. This project learns from its architecture, but our implementation and wording are independently written. No bundled upstream program files, fonts, or logos were copied.

## What was inspected

Inspected the upstream README, CLAUDE.md, SETUP.md, main skill and source-adapter playbooks, search/detail CLI conventions, `/setup`, `/scrape`, `/rank`, `/apply`, `/outcome`, `/expand`, `/add-portal`, `/add-template`, `/gmail-sync`, `/html-report`, job eligibility framework, search escalation rules, rank-state helper, canonical job keys, privacy/security guardrails, robots gate, PDF/layout verification, and representative unit tests. The original has 310 Git tree entries including six portal skills and a much larger regression suite. This is an architecture/behaviour study, not a claim to have performed every upstream integration test.

## Detailed translation table

| Upstream subsystem | Grounded design principle | Funding Autopilot translation |
| --- | --- | --- |
| `/setup` and `01-candidate-profile.md` | Long-lived verified profile; input conflict resolution; user-approved updates | Mandatory uploaded CV; private applicant evidence ledger; split observed/confirmed/expected milestones; versioned CV hash |
| `/expand` | Enrich profile from linked documents and public GitHub/projects while distinguishing inference | Proposal-safe enrichment from papers/repos/institutional pages, with original source pointers and human approval |
| Portal search skills (search/detail) | Modular market-specific adapters, stable JSON result schema, access/health errors | Modular **official funder** source adapters with discovery vs full-call verification and explicit rule provenance |
| `/scrape` | Store every discovered candidate and provenance; avoid duplicates; preserve excluded results | Stable (funder, official programme ID, round) key; store unverified leads; never silently erase history |
| `/rank` and `tools/rank_state.py` | Cheap bounded triage separated from deep authoritative review; stable source state; deadline sweep | Batch local lead selection, route-specific hard eligibility gate, fit heuristic only after evidence, institution/internal deadline precedence |
| `/apply` | Draft → independent content reviewer → revise → compile → inspect; record drafted ≠ submitted | Funder-specific proposal sections, independent eligibility and scientific reviewers, formal word/page checks; `draft_ready` is not submission |
| `/add-template` | Template manifest declares format and compiler; test-compile before activation | Funder-format manifest, document-specific word/character/page budgets, test-render and PDF/text layer inspection where supported |
| `/outcome` | Archive what was really submitted, status timestamps, rejection/offer history; follow-up drafts never sent | Private complete application packet + receipt, under-review and award/rejection outcomes, user-confirmed status changes and feedback for next round |
| `/gmail-sync` | Match inbox messages to known applications, request approval before committing status; contradictions go to manual review | Optional grant-office and funder-response classification, source email citations, **approval-only changes**, no automatic claims of awards |
| `/html-report` | Self-contained local HTML and cross-application visibility | Offline status/deadline dashboard with escaped third-party content and no external assets |
| `/add-portal` | Connector generation with contract, test query and access/robots checks | `add-source`: source manifest + rights checks + a live test of official scheme page; no credential bypass |
| Security/robustness tests | No automatic hooks, private paths protected, no silent truncation or invented facts | Required ignored `private/`, no Actions/workflows/hooks, no personal-data GitHub writes, reversible explicit transitions, atomic local ledger |

## Differences we deliberately retain

1. **Funding eligibility is not job fit.** Check PI authority, fellow eligibility, host acceptance, PhD submission vs awarded date, funder and institution deadlines, cost policy and salary eligibility. Unknown is conditional/unverified, never a numeric pass.
2. **Grants have rounds and nonportable host rules.** Funding identity includes round. A change of receiving institution requires a new internal deadline/approval review. A funder call may support collaboration without paying the applicant.
3. **Official guidance controls the form.** Funder-specific forms, assessment criteria and budget categories outrank a generic proposal template; open-source LaTeX CV page limits do not apply to every grant.
4. **No fake autonomous browsing.** The host with approved web tools fetches official source content. The Python CLI is a state/eligibility helper, not a built-in live scraper or an unattended agent.
5. **Public repository remains generic.** A real CV, profile, drafts, host correspondence and tracking ledger stay under `private/` and must not be published. A user may separately authorize sharing a sanitized example.
6. **No GitHub Actions.** The reference repo ships CI and watch workflows; Funding intentionally uses ordinary direct Git reads and guarded pushes only. A real external scheduler must be authorized separately.

## Measurable acceptance targets

- Without uploaded CV, no personalized ranking or proposal.
- With only search snippets and no fresh official call evidence, no `eligible` verdict.
- "Expected thesis submission" never satisfies "already submitted" or "PhD awarded".
- Overlapping sources and changed titles preserve one stable call per round.
- A programmatic batch does not dump the lifetime ledger into the model context or discard deferred opportunities.
- A strong fit score cannot override an impossible lead/PI route, missing host or earlier internal deadline.
- A draft is never marked `submitted` and an outcome never marked `awarded` without user confirmation and a receipt/reference.
- An offline report never executes HTML or loads remote assets based on third-party scraped text.
- All new code and examples are standalone and fictional; upstream attribution remains present.
