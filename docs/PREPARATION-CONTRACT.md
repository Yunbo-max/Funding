# Preparation before a funding application

**Match → Prepare → Apply** is a deliberate dependency. A researcher cannot write a persuasive proposal simply because its funding call matches some keywords.

## Outputs of Prepare

**1. Research strategy.** The scientific or impact problem, hypothesis, distinctive mechanism, strongest alternatives, feasible comparisons, and milestones. Tailor the logic to the funder's actual criteria.

**2. Applicant evidence.** Verified CV facts and publications, with page/section references or primary source links. Original achievements cannot be invented or overstated.

**3. Host and budget.** Clearly identify whether the applicant can lead individually, needs a mentor, or needs a new PI/receiving institution. Check internal approvals, project vs personal salary funding, cost sharing and institutional costing.

**4. Exact form outline.** For every required form section, record its verified word/page limit, its intended claim, source evidence, associated work package and supporting document. Unresolved questions remain visible.

## Local sequence

```bash
python3 skills/funding-autopilot/scripts/workspace.py match
python3 skills/funding-autopilot/scripts/workspace.py prepare --key call-VERIFIED-KEY --route independent
```

This creates private `preparation.md`, `preparation.json` and required-document checklists (plus an **unsent** PI outreach draft for a new-PI route). The Agent fills them using current official guidance and uploaded CV facts. The preparation JSON must include `research_question`, `distinctive_approach`, `feasibility_and_evaluation`, `evidence_fact_ids` of **user-confirmed** CV facts, required `section_outlines`, `host_plan`, `budget_plan` and `unresolved_requirements`.

```bash
python3 skills/funding-autopilot/scripts/workspace.py prepare-complete --key call-VERIFIED-KEY --confirm-reviewed
python3 skills/funding-autopilot/scripts/workspace.py apply --key call-VERIFIED-KEY
```

The second command only becomes available when the actual applicant has reviewed the strategy. The first check establishes structural integrity, not scientific correctness. Conditional PI/Host routes can produce exploratory drafts, but not submission-ready proposals. **No email or application is submitted automatically.**

## Why this differs from a job application

A research grant often has a separate problem-definition and Host/PI contracting stage, a stricter budget and a score rubric tied to the proposal's science. Funding Autopilot therefore treats proposal preparation as its own milestone rather than as the first paragraphs of Apply.
