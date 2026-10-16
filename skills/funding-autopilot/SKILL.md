---
name: funding-autopilot
description: "Use when a researcher uploads a CV and wants to discover real grants, fellowships, postdoc funding, prizes or PI partnerships, verify applicant/host eligibility and deadlines, compare funding routes, or draft and revise evidence-backed funding applications."
license: MIT
compatibility: "Requires a host able to read uploaded CVs and browse current official funding pages; optional local Python 3.10+ helper."
metadata:
  author: Yunbo-max
  version: "0.4.0"
---

# Funding Autopilot

Find a suitable *eligible* funding route, then develop the strongest honest application supported by the applicant's evidence. Treat opportunities as **funder-specific contracts**, not generic topic keywords. This skill operates on demand; it does not schedule itself or send applications.

## The workflow (keep this order)

### Gate 0 — Require user-uploaded CV and preserve privacy

- **CV upload is mandatory** for personalized search, recommendation, and drafted application. Accept PDF, DOCX, Markdown or text. A homepage/LinkedIn/ORCID alone cannot satisfy this gate. If no CV is attached, request one and stop personalized stages; general source guidance remains allowed.
- Read [intake and privacy](references/intake-and-privacy.md). Extract only CV-grounded facts, with page/section/text-span pointers; distinguish observed, user-confirmed, inferred, unknown. Do not assume all CV content remains current.
- Build an applicant record: career stage *now* and at proposed start, thesis submitted vs degree awarded, discipline, verified output, preferred research direction, geography, salary need, independence/new-PI route, work/host constraints. Use previously supplied constraints; ask only for genuinely consequential missing details.
- An uploaded CV is private. Do not upload it to a public GitHub repository, a third-party funding site or an unapproved AI service. Store local applicant records only in ignored private paths. If access to the upload is unavailable, do not pretend to have read it.

### Gate 1 — Search multiple funding pathways

Read [discovery](references/discovery.md), then use actual web/search tools to query **official funder pages** in multiple keyword and eligibility families inferred from the CV. Search at least: personal fellowships; independently led research grants; grants with a **new PI or host**; collaborative/programme calls; and research prizes only if they serve the user's goal. Do not constrain the researcher to their current supervisor, institution or discipline if the user seeks to move.

Use [source-registry.json](assets/source-registry.json) only as initial search portals, *not* as a live opportunity list. Include regional sources relevant to the user. Query target official call pages, PDF guidance and institution-side internal funding office notices. De-duplicate by official call ID + round, not merely by title.

### Gate 2 — Verify before presenting eligibility

Read [eligibility](references/eligibility.md). For each shortlisted call, retrieve the exact **current round** and retain its URL, checked-at UTC timestamp, relevant rule section, and evidence for:
- applicant type and permitted role (lead/PI, fellow, employee, collaborator, student);
- thesis **submitted** versus PhD **awarded**, by which date, and years since PhD;
- eligible organisation, host, mentor/PI commitment, employment conditions, mobility and geography;
- research scope, salary/eligible costs, funding size and duration when confirmed;
- external funder deadline **and** applicable university/department/internal approvals and deadlines;
- required documents, forms, page/word limits, review criteria and intellectual-property/open-science obligations.

If an important rule is unresolved: **conditional** if a concrete approval/fact is missing; **unverified** if primary evidence is missing/stale; **ineligible** for a known hard violation; **expired** for passed valid deadlines. Do not present a relevance score as a probability of being awarded. New-PI route may be plausible without the current supervisor, but remains conditional until the new PI/host agrees.

### Gate 3 — Decide and shortlist

Offer the independent, new-PI, and fellowship/postdoc routes as distinct options. For each opportunity report: status, concrete reason, role, host required, allowed salary, official sources, verified-on date, earliest applicable deadline, unresolved gates, project fit and requested next action. Rank only verified-and-eligible options together; show conditional options separately. Explain conflicts or unknowns rather than silently discounting them.

Use [records](references/records.md) for machine-readable representations. The local script can check conservative gates for structured official-call data, but it **does not perform web research or certify official-source authenticity**.

### Gate 3.5 — Prepare the research before Apply

**Match is not Prepare; Prepare is not Apply.** Select a specific officially verified current-round call and an independent or new-PI applicant route. Run **workspace.py prepare --key CALL_KEY --route independent|new_pi** to generate a private strategy packet. This does **not** create a proposal draft.

Read [the preparation module](commands/04-prepare.md) and [the plan contract](references/preparation.md). The AI host must fill the substantive research problem/approach/evaluation, map user-confirmed CV evidence to each required official form section, record real new-PI/Host and salary/budget conditions, materials, risks and unresolved institutional approvals. A proposal scaffold or placeholder is not an approved strategy.

Present the plan to the applicant. Only after explicit approval, run **workspace.py prepare-complete --key CALL_KEY --confirm-reviewed**. The local checker enforces plan/CV/call identity and required sourced field structure but cannot guarantee scientific novelty or Host acceptance. Conditional opportunities may proceed as exploratory concepts; they cannot become submission-ready until eligibility requirements are met.

### Gate 4 — Write to the *exact funder form*

Only after a selected opportunity and applicant route have an explicitly reviewed **prepared** strategy, read [proposal writing](references/proposal-writing.md) and [proposal template](assets/proposal-template.md). Load the original scheme guidance, the latest forms, evaluation rubric and verified CV facts, plus real research outputs the user authorizes. Prepare the outline/requirements matrix first.

Develop a rigorous research narrative: problem and relevance to the funder; gap and strongest prior approach; original question, theoretical or empirical mechanism and falsifiable hypothesis; feasible work packages, milestones, outcomes and risk; why this applicant/new PI/host; evaluation and impact; defensible budget. Borrow Research Autopilot's *evidence → prediction → method → comparative test → interpretation* reasoning, not its entire runtime or mechanical mathematics traversal. No fabricated results, collaborations, matched funds, ethics approvals or impact.

Create a source-linked claim ledger. Use explicit `[EVIDENCE NEEDED]`, `[TO CONFIRM]` and `[HOST APPROVAL REQUIRED]` placeholders. Keep unverified claims out of final-ready text. Compose separate PI outreach, host request, CV tailoring and budget notes only when relevant. Drafting outreach is allowed; **sending requires user approval**.

### Gate 5 — Review, repair, deliver

Perform **two passes**: (a) a skeptical eligibility/compliance reviewer checks against official call and internal institutional rules; (b) a scientific reviewer checks merit, innovation, feasibility, comparators, claims and risk. Check section lengths, citations, dates, ethics/data, evidence gaps, deliverables and role/host. Revise only supported claims. A programmatic audit helps detect omissions, not guarantee compliance.

A deliverable package includes: (1) ranked funding matrix, or a chosen call; (2) eligibility and missing-approval checklist; (3) evidence links/checked date; (4) editable call-shaped proposal documents; (5) requirement-to-section trace; (6) red-team feedback and unresolved items. Mark every packet **DRAFT — HUMAN AND HOST REVIEW REQUIRED** until a human reviews it. Submission requires explicit authorization.

### Updates and recurrence

When the user explicitly asks for recurring discovery or deadline alerts, set a real host-supported scheduler and preserve source/review state. An ordinary chat response or git commit does not create unattended execution. Never use GitHub Actions. Persist only sanitized project logs to GitHub if the user requests it; never private CVs or applications.

## Optional helper

```bash
python3 skills/funding-autopilot/scripts/funding.py intake --cv private/cv.pdf --out private/profile.json
python3 skills/funding-autopilot/scripts/funding.py shortlist --profile private/profile.json --calls private/calls.json --out private/shortlist.json
python3 skills/funding-autopilot/scripts/funding.py prepare --call private/verified-call.json --out private/application-draft.md
python3 skills/funding-autopilot/scripts/funding.py audit --proposal private/proposal.json --call private/call.json --out private/audit.json
```

PDF extraction needs the optional pypdf package; DOCX needs python-docx. A successful intake means *text was extracted*, not that the agent has confirmed career facts. Read [records](references/records.md) before populating the structured JSON.

**Stop rules:** No uploaded CV → no personalized matching/writing. No official call evidence → no verified eligibility claim. No confirmed host when compulsory → not eligible yet. No adequate evidence for a research claim → narrow or mark it missing. User withdrawal or stop → stop.

## Modular application operating system

Use the appropriate command playbook on demand; all commands inherit the mandatory CV/privacy, official-evidence and human-approval gates above:

- [setup](commands/01-setup.md) — private, provenance-backed researcher profile;
- [discover](commands/02-discover.md) — source adapters, search/dedup, full-call retrieval;
- [rank](commands/03-rank.md) — bounded triage and independently verified eligibility;
- [apply](commands/04-apply.md) — exact official form, independent reviewers and rendered-document checks;
- [outcome](commands/05-outcome.md) — receipts and longitudinal improvement;
- [add-source](commands/06-add-source.md) — opt-in official portal adapter generation and validation;
- [expand](commands/07-expand.md) — source-grounded CV augmentation with user approval;
- [report / inbox](commands/08-report-and-inbox.md) — private offline dashboard and opt-in approved updates.

When a local runtime exists, use [the private pipeline record contract](references/pipeline-records.md) and `scripts/pipeline.py` for stable dedup, batch selection, distinct application stages, explicit outcome receipts and private report generation. Adapted from concepts in [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search); no upstream workflow code or GitHub Actions are imported. A tool's existence does not mean the user has launched a continuing process.

## Source adapter currently bundled

[UKRI official RSS](sources/README.md) provides public lead discovery via `sources/ukri_rss.py search` and cautious `detail` retrieval. Its RSS results are *not verified calls*: send them through the normal current-round official-guidance and internal-deadline gates. The feed covers only currently syndicated entries, not the complete UKRI catalogue. No applicant CV travels in RSS requests.

## v0.3 user experience: setup, find, rank, apply, track

Prefer the **real workbench** over asking users to manually stitch together unrelated Python commands. The canonical CLI is [`scripts/workspace.py`](scripts/workspace.py), which integrates CV intake, reviewed profiles, feed/source leads, verified round promotion, route-specific eligibility, application packet scaffolds and recorded outcomes. The supported Claude Code slash commands are in the repository's `.claude/commands/`; other skill-enabled hosts can use the same instructions in natural language.

**Interactive `/setup`:** an actual uploaded CV is mandatory. After parsing, the host should write CV-grounded education, publications, awards, projects and methodological facts with exact page/section locators into `private/cv-facts.json`, then run `workspace.py setup-facts --input-file private/cv-facts.json`. Proposed facts are **not confirmed** until the applicant reviews them. Run `workspace.py setup --cv <path> --topics "<CV-supported areas>"`, present `setup-review`, then run `setup-confirm --confirm-reviewed` only if the user explicitly accepts the facts. Later profile changes use `setup-update` without another CV upload, and reset review status until reapproved.

**`/search`:** use a genuine permitted UKRI RSS fetch or import other official funder leads gathered by host browsing. Read complete source guidance and promote provisional `round=unverified` leads through `workspace.py verify --key <key> --call-file <official-guidance-record.json>`. Repeated sightings of the same round/URL should not create fake fresh opportunities; recheck the official round.

**`/rank`:** re-run the concrete requirements, including user preference, PI/host, degree milestone, salary possibility and new receiving institution's deadlines. Never score a missing PI approval as eligible. Call `workspace.py rank` after current-round verification.

**`/apply`:** call `workspace.py apply --key <key> --route independent|new_pi` to create the **private** call-shaped proposal scaffold and PI outreach draft if relevant. Then the **AI host must actually draft the complete required proposal sections**, with verified CV and literature evidence, budget constraints, independent content critique, compliance audit and actual rendered-document inspection as applicable. An empty scaffold is *not* a complete application.

**`/outcome`:** `workspace.py ready` only after an audited and approved structured draft; actual submission/decision requires separate documented receipts and user confirmation. `workspace.py status` and the offline pipeline HTML report expose the private timeline.

This workflow is on-demand only. The Python CLI does **not** contain an LLM, does **not** contact unregistered funding portals, does **not** submit to funding portals and does **not** run perpetually. See [complete user walkthrough](../../docs/USER-WORKFLOW.md) and [v0.3 validation notes](../../docs/VALIDATION-0.3.md).

## Canonical v0.4 journey

**/setup → /search → /match → /prepare → /apply → /outcome**. Legacy /rank remains an alias for /match. The Python pipeline enforces a preparation stage between selected funding and proposal writing. See the [six-stage README diagram](../../assets/workflow.svg). It is a static illustration, not a running Web UI.
