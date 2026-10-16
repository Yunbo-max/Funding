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
