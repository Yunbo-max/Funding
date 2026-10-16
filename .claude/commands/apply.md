# /apply — Author a real, funder-specific research application

Read `skills/funding-autopilot/commands/04-apply.md`, `references/proposal-writing.md`, `references/records.md` and the current official call. Use `$ARGUMENTS` for the grant selection/route.

**Crucial:** running the CLI alone creates an honest *blank scaffold*. The AI drafter must actually write the application body from CV, verified papers and funder criteria, rather than stopping at "template generated."

1. Require an uploaded-CV setup confirmed by the user, a vetted current-round call and a separately chosen independent or new-PI application route. The call must be `eligible` or explicitly `conditional` for an exploratory concept; conditional calls cannot become submission-ready.
2. Run:
```bash
python3 skills/funding-autopilot/scripts/workspace.py apply --key call-EXACT-KEY --route independent
```
Change to `--route new_pi` for a new host/PI; do not silently choose the current supervisor.
3. Read `private/applications/<key>/<route>/proposal.md` and `requirements.md`. Fetch the **actual funder form**, read its scoring criteria and word/character/page limits, and gather CV- and publication-grounded evidence. Draft genuine sections: title/abstract, specific aims, mechanism and novelty, alternatives/baselines, research plan/evaluation, work packages/timeline, host fit and independence, broader impact, budget justification, risks/contingency and data/ethics as required. This is a writing task, not a bibliography scraper.
4. Produce full editable Markdown plus `proposal.json` using the exact `sections`, `documents`, `claims`, `evidence_index`, and `approval` schema from the chosen call and `references/records.md`. Place real sections under their official IDs, not placeholder summary text. Keep all files in ignored `private/`.
5. Conduct two independently focused reviews: **eligibility/compliance** and **scientific rigor**. If the host has true independent subagents, use them; otherwise clearly mark a separate critical review pass. Revise precise problems and preserve unknown facts. Never invent pilot results, employer salary, collaborator agreements, matching funds or impact evidence.
6. Run `funding.py audit --proposal private/<actual-proposal-json> --call private/<exact-official-call-json>` and compile/render actual DOCX/PDF only if requested and supported. Check rendered pages, tables, page limit, readability and source alignment; use `verify_grant_pdf.py` for mechanical checks but it cannot replace visual review.
7. Keep `[EVIDENCE NEEDED]`, `[TO CONFIRM]` and `[HOST APPROVAL REQUIRED]` in drafts until legitimately resolved. Do not mark ready while any required approval is missing.
8. With actual applicant/PI/host review and exact evidence/audit complete, the user may explicitly request:
```bash
python3 skills/funding-autopilot/scripts/workspace.py ready --key call-EXACT-KEY --proposal-json private/<actual-proposal-json> --confirm-reviewed
```
This records a reviewed draft, **not** a submitted application. For new-PI routes, prepare the separate unsent outreach draft and verify consent. Only a human-authorized portal process can submit.

Always finish with the actual editable deliverables, eligibility notes, review defects and a clear **NOT SUBMITTED** status until an external receipt is recorded.
