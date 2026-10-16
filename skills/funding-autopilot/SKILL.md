---
name: funding-autopilot
description: "Use when a researcher uploads a CV and wants to discover real grants, fellowships, postdoc funding, prizes or PI partnerships, verify applicant/host eligibility and deadlines, compare funding routes, or draft and revise evidence-backed funding applications."
license: MIT
compatibility: "Requires a host able to read uploaded CVs and browse current official funding pages; optional local Python 3.10+ helper."
metadata:
  author: Yunbo-max
  version: "0.1.0"
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

### Gate 4 — Write to the *exact funder form*

Only after a specific opportunity and application path are chosen, read [proposal writing](references/proposal-writing.md) and [proposal template](assets/proposal-template.md). Load the original scheme guidance, the latest forms, evaluation rubric and verified CV facts, plus real research outputs the user authorizes. Prepare the outline/requirements matrix first.

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
