# Funding Autopilot

**CV-grounded funding discovery, eligibility verification, and evidence-backed proposal writing.**

Funding Autopilot is an open-source [Agent Skill](https://agentskills.io/specification) for researchers and AI assistants. It starts with an **uploaded CV** and a funding goal, discovers real calls on official funder websites, checks applicant and host eligibility, and drafts funder-specific applications with auditable evidence. It is a skill for an AI host with search and document-reading tools, **not** a live grant database or a background service.

> **Important:** A topic match is not an eligibility decision. An applicant who has *submitted a PhD thesis* has not necessarily been *awarded a PhD*. A different PI, mentor or host institution may be possible, but requires call-specific and institutional verification.

## What it does

1. **CV intake** — requires user-supplied PDF, DOCX, Markdown or text CV; extracts relevant, source-backed achievements and career stage, asks only for consequential missing constraints. Public profile links can supplement but not replace a CV.
2. **Opportunity discovery** — searches UK/European/US/global funders, discipline-specific schemes, fellowships, independent awards and partner-led grants, using multiple keyword families derived from the CV.
3. **Eligibility gates** — separates individual applicant, fellowship holder, project lead/PI, team member, mentor, institutional host and employer; tracks PhD submission vs award, nationalities/residence when required, geography, host approval, work eligibility, career limits and all deadlines.
4. **Explainable shortlisting** — shows only evidence-verified candidates as eligible; classifies conditional, ineligible, expired and unverified calls separately, without treating an unknown as a pass.
5. **Proposal studio** — prepares research concept notes, funder-specific narrative sections, work packages, impact/pathways, open-science/data plans, budget justifications, cover letters and PI outreach drafts with a requirement-to-evidence trace.
6. **Review/repair loop** — tests against official call text, word/page limits, required documents, institutional approval, policy and unsupported claims, then revises the exact missing items.

Inspired by the **evidence → decision → review → revision** practices of [Research Autopilot](https://github.com/Yunbo-max/Research_Autopilot), but deliberately independent: **no GitHub Actions, scheduled jobs, workflow runs or external API keys are required**.

## Quick start

Install the skill directory `skills/funding-autopilot/` in an Agent Skills-compatible host (for example a configured local or project skills directory), then ask:

> Use Funding Autopilot. I uploaded my CV. Find grants or postdoctoral fellowships I could pursue without staying in my current research group, including an independent route and a route with a new PI. Verify actual eligibility and internal deadlines before ranking; draft only for the opportunities I select.

The host needs web/search access to discover *current* opportunities and document-reading support for the uploaded CV. The skill does **not** claim internet discovery can happen from its offline Python helper alone.

For local structured checks (Python 3.10+, standard library), run:

```bash
python3 skills/funding-autopilot/scripts/funding.py intake --cv path/to/cv.pdf --out private/profile.json
python3 skills/funding-autopilot/scripts/funding.py shortlist --profile private/profile.json --calls examples/illustrative-calls.json --out private/shortlist.json
python3 skills/funding-autopilot/scripts/funding.py prepare --call private/verified-call.json --out private/application-draft.md
python3 skills/funding-autopilot/scripts/funding.py audit --proposal private/proposal.json --call private/verified-call.json
python3 -m unittest discover -s tests -v
```

The intake extractor needs `pypdf` for PDF or `python-docx` for DOCX (`pip install -e '.[documents]'`). If either parser is absent, it fails visibly; scanned/image-only PDFs must be checked manually. `intake` yields a conservative **unverified profile** for agent review, not a fabricated career history. The sample calls are fictional and must never be presented as open funding.

## Repository layout

```text
skills/funding-autopilot/
  SKILL.md                  # agent entry point and gates
  references/
    intake-and-privacy.md   # CV evidence and permissions
    discovery.md            # sources, search, verification
    eligibility.md          # hard constraints and unknowns
    proposal-writing.md     # application composition and review
    records.md              # data contracts and examples
  assets/
    source-registry.json    # starting points; not a live calls feed
    proposal-template.md
  scripts/funding.py        # local checks; never claims web verification
tests/test_funding.py
examples/illustrative-calls.json
docs/README.zh-CN.md
```

## Evidence and safety contract

- Every current deadline, eligibility rule, award amount and application format must link to the **specific official call page or official document** and carry a checked-at timestamp. Check departmental/internal submission dates separately; the funder deadline alone is not enough.
- Distinguish **discovered**, **verified**, **eligible**, **conditional**, **ineligible**, **expired**, **unverified** and **draft/not submission-ready**. Do not infer eligibility from a search snippet or similarity score.
- Never invent papers, awards, citations, preliminary results, named collaborator commitments, ethics approvals or figures. Unknowns remain explicit `[TO CONFIRM]` or `[EVIDENCE NEEDED]`.
- Never upload a CV or private proposal to a public repository without explicit approval. The default `private/`, `applications/`, `output/` and `logs/private/` paths are ignored by Git. Logs published to GitHub must be sanitized.
- Do not submit applications, impersonate a PI, contact hosts or claim an appointment without explicit user authorization. Writing a draft does not establish a funding decision or a job offer.
- No autonomous recurrence is implied: a real host scheduler must be set up separately when requested.

## Development

The helper handles deterministic extraction, conservative eligibility classification, and document structure audit. The host agent performs fresh web discovery, reads PDFs/official call documents, reasons about research fit and writes prose. This division keeps source verification separate from automation claims.

Contributions and new funding-source adapters are welcome. Add test fixtures rather than real CVs. See [the skill](skills/funding-autopilot/SKILL.md) and [Chinese guide](docs/README.zh-CN.md).

License: MIT.

## Stateful application workflow (v0.2)

The system also adopts a staged **setup → discover → rank → apply → outcome** workspace pattern, inspired by [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search). This is an independently implemented grant-specific design: unlike job search, *verified funder/PI/host eligibility overrides topic fit*. See [the upstream architecture study](docs/UPSTREAM-DESIGN-STUDY.md), [private ledger specification](skills/funding-autopilot/references/pipeline-records.md), and [command modules](skills/funding-autopilot/commands/).

New (local, non-network) pipeline commands:

```bash
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json ingest --input private/discovered-calls.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json batch --limit 10
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json rank --profile private/profile.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json report --out private/funding-report.html
```

These tools manage **private leads, evaluations, progress and an offline report**, not live grant scraping or submission. The AI host still has to retrieve and interpret current official funder guidance. Progress transitions that claim submission or an award require explicit confirmation and evidence. The originating job-search project remains MIT-licensed and credited; we do not ship its source files or workflow actions.
