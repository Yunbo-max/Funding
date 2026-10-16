# Preparation contract

## Why it exists

**Match** evaluates official eligibility and fit. **Prepare** decides what credible research to propose, with what evidence, Host/PI, budget and scheme-specific structure. **Apply** writes, reviews and formats actual application documents. Those stages have distinct decisions and records.

## Deterministic states

The local sequence is **selected → preparing → prepared → drafting → draft_ready**. A plan must be explicitly approved before prepared is recorded, and later submission needs a separate real portal receipt. Legacy rank is an alias of match.

**prepare** creates private/applications/CALL_KEY/ROUTE/preparation.md and preparation.json, scheme requirements.md and an optional new-PI unsent outreach draft. These are working preparation artifacts, **not** completed proposal documents. The AI host fills them using the current official call and CV fact ledger.

**prepare-complete** requires user confirmation and checks that the JSON plan names the exact call key, funder call ID, round, route, verified official timestamp and CV hash. It requires meaningful research_question, distinctive_approach, feasibility_and_evaluation, every required scheme section_outlines entry and at least one user_confirmed CV evidence_fact_id. Host_plan and budget_plan remain explicit even if approval or costing is pending, and unresolved_requirements remain visible.

The built-in checker establishes only basic integrity and minimum structure. It cannot establish scientific truth, novelty, full institutional eligibility, budget correctness or authentic PI agreement. Complete critical scientific and compliance review occurs during Apply.

## Personal research narrative: background → direction → fit

Before producing the plan, answer five questions using **specific CV evidence and the applicant's confirmed preferences**:

1. **What is distinctive about this researcher?** Identify their actual contributions and transferable capabilities—not prestige, publication count alone, or an inferred skill.
2. **What question follows naturally from their past work?** Find a research direction that makes intellectual sense given their experiences, including non-linear or cross-disciplinary paths.
3. **Why does this funding route fit that direction?** Compare plausible alternative research framings and independently viable or new-PI/host pathways, rather than searching only for the closest keyword.
4. **Why this applicant, this project, this funder, now?** Build a coherent funder-specific argument from **verified past work → precise problem → testable future contribution → public programme priorities**.
5. **What might defeat that narrative?** Identify missing data, weak baselines, a better-aligned funding call, uncertain applicant/host eligibility, overly ambitious work packages, or claims the CV does not support.

Write these as a **short narrative rationale** in the human-readable private `preparation.md`, while using the structured `preparation.json` research question, approach, evaluation, fact IDs and section outlines for machine checks. Show alternative possible directions where genuinely supported; let the applicant choose. **Never bend the facts to fit a funder, assume collaboration consent, or transform a proposed future result into a completed achievement.**

## Required plan keys

| Key | Source and meaning |
| --- | --- |
| call_key, call_id, round, route | Exact officially sourced scheme and chosen route |
| cv_sha256, official_call_checked_at | Pinned evidence sources; cannot silently swap CV or call version |
| research_question | Scientific or impact question appropriate to the funder |
| distinctive_approach | Main research idea and comparison to alternatives |
| feasibility_and_evaluation | Work packages, feasibility, baseline/metrics and timeline |
| evidence_fact_ids | User-confirmed CV facts stored in the private profile |
| section_outlines | Substantive outline for **every** required official form field |
| host_plan | PI, Mentor, institution and signed-support gaps |
| budget_plan | Salary, allowed expenditure and institution costing gaps |
| research_risks, unresolved_requirements | Explicit unresolved research and administrative blockers |

## Route distinctions

An independent fellowship can still require a receiving host or mentor. A new-PI-led grant may pay a postdoctoral salary only when allowed by the specific budget rules. A conditional route may be explored and drafted, but must not be labeled eligible or submission-ready while mandatory approvals remain outstanding.

## Safety

All preparation files remain in ignored private/ directories. The user may approve a strategy without authorizing messages or a grant submission. No GitHub Actions, workflow dispatch or automatic sending.

## Different calls require different research arguments

Read [the grant writing matrix](../../../docs/PROPOSAL-STRATEGIES.md). Choose applicant independence for fellowships, scientifically falsifiable mechanisms for project grants, contractual partner roles for consortia, validated need for innovation, and real measured external outcomes for impact awards. Use the particular funder's current requirements over these general patterns.
