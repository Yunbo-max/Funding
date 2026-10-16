# Repository instructions

This is the public, CV-grounded Funding Autopilot Agent Skill. The canonical entry point is [skills/funding-autopilot/SKILL.md](skills/funding-autopilot/SKILL.md).

- The user must provide a CV before personalized funding discovery and proposal authoring. A URL to a website, social profile or citation database does **not** replace the CV.
- Keep CVs, extracted text, applicant profiles, contact details, proposals, application materials and private project data local and ignored by Git. Never commit, publish or email these without explicit authorization.
- For every funding recommendation, fetch the *specific official call* and cite rule/amount/deadline/format evidence, dated as of the actual read. Check institution-specific deadlines and host or supervisor eligibility. Unknown is not eligible.
- Treat thesis submission, PhD award, contract/employment status, host acceptance, PI eligibility and ability to start the grant as distinct facts.
- The skill provides instructions; the host agent performs live browsing and writing. Python standard-library helper supplies deterministic checks only. It cannot discover live grants by itself.
- Adapt Research Autopilot's source/evidence/decision/revision/negative-evidence loop, not its research runner, automatic continuation or large research database. No GitHub Actions, workflow runs or workflow_dispatch; use direct fetch and guarded commits only when updating this repo.
- Drafts, outreach and budgets may be generated; submission, contact, spending and actual employment promises require explicit human approval.
- Do not invent papers, hosts, funding amounts, success probabilities, authorizations, approvals or experiments. Never claim a working scheduler that has not been installed and verified.
- Run local unit tests before releases. Record actual test commands and exit codes; commit only sanitized maintenance notes. If GitHub synchronization cannot be verified, produce a downloadable ZIP if the host supports it and mark sync pending.

## v0.3 public multi-user workbench

Native slash commands under `.claude/commands/` use `skills/funding-autopilot/scripts/workspace.py`. The existing `funding.py`/ `pipeline.py` helpers remain source of record for actual gating. Setup creates a private, unreviewed profile; only a documented user review may call `setup-confirm`. Updating a research direction or host preference through `setup-update` must not erase the uploaded CV hash, ledger, previous grants or previous decisions, and must reset reviewed status.

Personal grant applications must have a real selected route, verified round, official guidance and documented review. The wrapper creates scaffolds; an authorized AI host must compose genuine grant prose and actual artifact files before telling the user the application is written. Never call an empty scaffold a finished proposal. Marking `draft_ready` is not submission; outcomes require receipts. Tests using fictional calls or stub dependencies must be reported as such and may not be described as real sponsor availability or validated end-to-end deployment.

All private records remain under an ignored `private/` path. Do not add GitHub Actions, .github/workflows files, automatic hooks or unattended web scrapers. Use direct reads and guarded commits only, with readback verification.
