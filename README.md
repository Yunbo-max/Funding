<p align="center">
  <img src="assets/hero.svg" alt="Funding Autopilot — from research ideas to funding applications" width="100%">
</p>

<h1 align="center">Funding Autopilot</h1>
<p align="center"><strong>Find funding worldwide. Verify eligibility. Prepare the research. Write the application.</strong></p>
<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#example-input--output">Example</a> ·
  <a href="docs/USER-WORKFLOW.md">Full guide</a> ·
  <a href="docs/README.zh-CN.md">中文</a>
</p>

**Funding Autopilot** is an open-source, CV-grounded **research funding discovery and application workflow**. It is designed for researchers across disciplines and regions: **UK, Europe, US, Canada, Australia, Asia, and beyond** — wherever relevant official funding information can be accessed and the applicant meets the scheme's rules.

Find individual fellowships, independent research grants, **opportunities with a new PI/host**, collaborative funding, research awards, and other relevant calls. It does not assume you must remain in your current research group.

> **Worldwide by design, not a worldwide live database.** With web access, an AI agent can research the official funding sources for the countries you select. The bundled standalone discovery connector currently covers **UKRI's recent RSS feed only**; other regions depend on the agent's web/search tools or additional source adapters. Coverage and eligibility vary by scheme.

## What makes it different?

- **Researcher-first, not keyword-first.** Your uploaded CV, actual achievements, career stage, research goals, desired location, salary needs, and independence preference inform the search.
- **Eligibility before ranking.** The agent checks the *specific official call and round*: who can apply, thesis submitted vs PhD awarded, individual vs PI-led routes, new host requirements, salary eligibility, and the **institutional deadline** as well as the funder's deadline.
- **Prepare before Apply.** It doesn't leap from “good match” to generic grant text. It develops a defensible research question, an evidence-backed approach, milestones, evaluation, PI/host plan, budget assumptions, and an outline for every required funder section.
- **Evidence → draft → critical review.** Proposals reuse verified CV facts, follow the actual funder form, surface missing evidence, and go through compliance/scientific review. Nothing is marked submitted or funded without real confirmation.

## How the agent decides

```text
CV evidence → search by region, field and career stage → official funder rules
   ├─ Ineligible  → record the reason; explore another scheme or route
   ├─ Uncertain   → check degree timing, salary, PI/host and internal deadline
   └─ Eligible    → prepare a testable research plan → write → review → revise
```

Decisions are **source-linked and revisited when new evidence arrives**, not predicted award probabilities. The workflow runs when you invoke it; it does not silently search or apply in the background.

## The workflow

![Setup → Search → Match → Prepare → Apply → Track](assets/workflow.svg)

| Step | Decision / output |
| --- | --- |
| **`/setup`** | Upload CV → save a private, user-reviewed research profile |
| **`/search`** | Generate targeted searches by field, career stage, funding type, and **country/region** → collect source-linked leads |
| **`/match`** | Read the official call → separate **eligible / conditional / ineligible / unverified** routes and deadlines |
| **`/prepare`** | Develop the research strategy, PI/host and budget plan, CV evidence map, and call-specific section outlines → **user reviews** |
| **`/apply`** | Write the actual proposal sections, criticize and revise, check requirements, generate editable application materials |
| **`/outcome`** | Record real submissions and decisions, with user confirmation and receipts |

`/rank` remains an alias of `/match`. `/status` shows saved progress.

## Quick start

Open the project in **[Claude Code](https://claude.com/claude-code)**:

```bash
git clone https://github.com/Yunbo-max/Funding.git
cd Funding
claude
```

Then follow the conversation-driven commands:

```text
/setup     → Upload your CV and review your profile
/search    → Find opportunities in your selected regions
/match     → Verify eligibility and choose an application route
/prepare   → Develop and review a call-specific research plan
/apply     → Write and review the proposal
/outcome   → Track the real submission and funding decision
```

You can also install [the Agent Skill](skills/funding-autopilot/SKILL.md) in a compatible host and use natural-language requests. **The Python CLI handles local data and checks; the AI host handles online research and substantive proposal writing.** [Full installation instructions](docs/INSTALL.md).

## Example: Input → Output

<details open>
<summary><strong>Input: CV + one research goal</strong></summary>

Upload `my-cv.pdf` and tell the agent:

> “I work on trustworthy AI agents and self-improving models. I expect to submit my PhD thesis in November 2026. Find research funding in the UK, Europe, US, Canada, Australia, or Singapore. I want to move to a new research group, and need a route that could pay my salary. Compare independent fellowships with grants led by a new PI. Check real eligibility and deadlines before recommending anything.”

</details>

<details open>
<summary><strong>Output A: Explained funding matches</strong></summary>

*Illustrative output format — **not live opportunities or real eligibility decisions**.*

| Route | Example status | What the agent needs to check |
| --- | --- | --- |
| Independent fellowship | **Conditional** | Whether a submitted thesis (rather than an awarded PhD) satisfies the call's date rule |
| Grant led by a new PI | **Conditional** | New PI/host acceptance, institution's internal deadline, and whether researcher salary is an allowable cost |
| Research prize | **Ineligible (example)** | An explicitly required completed degree or other disqualifying criterion |

For real results, each row also includes the **official source URL, exact rule, funding round, date checked, and next action**. “Conditional” never means “eligible.”

</details>

<details open>
<summary><strong>Output B: Preparation → application files</strong></summary>

Once you select and verify a real funding round, the agent prepares a research strategy and required documents:

```text
private/                               # git-ignored; never published
├── profile.json                       # CV facts, goals, PhD/host status
├── ledger.json                        # calls, evidence, eligibility, deadlines
└── applications/
    └── call-…/independent/
        ├── preparation.md             # research question, methods, PI, budget
        ├── preparation.json           # structured plan & CV evidence IDs
        ├── requirements.md            # official form and approval checklist
        ├── proposal.md                # funder-specific draft (after Prepare)
        └── application.json           # status: drafting, NOT submitted
```

**Prepare** must contain a substantive, applicant-reviewed strategy before **Apply** is unlocked. The AI host then writes and reviews actual proposal text; the Python command alone only creates the section scaffold. Final submission remains a separate, human-authorized action.

</details>

## Built-in vs agent-powered

| Available in the repository | Requires a connected AI host / human |
| --- | --- |
| CV text extraction, private profile/ledger, deterministic eligibility checks, preparation gates, draft scaffolds, UKRI RSS lead adapter | Global official-site research, checking current PDFs/FAQs and host rules, scientific reasoning, full proposal writing, document rendering and approvals |

**Privacy:** CVs, unpublished research ideas, budget details, PI correspondence, and proposal drafts remain in local `private/` paths (ignored by Git). The repository includes **no GitHub Actions, workflow runs, automatic email, or grant submission**. A Skill alone cannot run continuously in the background.

## More

[Complete workflow](docs/USER-WORKFLOW.md) · [Preparation contract](docs/PREPARATION-CONTRACT.md) · [Funding source adapters](skills/funding-autopilot/sources/README.md) · [Developer and validation notes](docs/) · [中文说明](docs/README.zh-CN.md)

Inspired by the workflow design of [AI Job Search](https://github.com/MadsLorentzen/ai-job-search) and the evidence-oriented research methodology of [Research Autopilot](https://github.com/Yunbo-max/Research_Autopilot). Independently implemented. **MIT License.**
