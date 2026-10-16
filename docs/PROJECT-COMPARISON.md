# Related projects and positioning

Reviewed against publicly available vendor documentation and repository READMEs on **2026-10-16**. These are **feature-positioning descriptions, not measured benchmark scores**. An unmentioned feature may exist; do not represent documentation silence as technical inability. There is no basis to call Funding Autopilot "the first" AI funding-discovery or grant-writing tool.

| Project | Publicly documented strength | Focus/trade-off relative to Funding Autopilot |
| --- | --- | --- |
| [Funding Autopilot](https://github.com/Yunbo-max/Funding) | Open-source CV profile, personal career-stage and PI/host eligibility reasoning, reviewed preparation, proposal-writing instructions and locally retained source/audit records | Globally **agent-assisted** search, not a proprietary or complete live database. Only bundled standalone UKRI RSS feed today. Full prose and global web browsing require an AI host. |
| [PaperBreak](https://paperbreak.ai/) | Research-specific live indexed grant discovery, eligibility analysis, budgets, application documents and compliance/review; published EU/UK/Germany coverage and supplied-call support internationally | Hosted full-service platform with substantive indexed opportunity coverage. Funding Autopilot differentiates on open-source **local data**, CV-grounded career transition, independent/new-PI/host/salary route checks and explicit preparatory scientific plan. |
| [GrantWell](https://github.com/The-Burnes-Center/AI4Impact-GrantWell) | US state/federal NOFO matching, requirements analysis, chatbot, collaborative document editor and administrative dashboard; AWS deployment | Stronger packaged application editor/UI; our repository is primarily a portable Agent Skill and a researcher's private local workflow, rather than a deployed NOFO SaaS. |
| [grant-finder](https://github.com/openprose/grant-finder) | Self-hosted US federal and select state funding discovery from official APIs/RSS, persistent source-cited records, deterministic retrieval | Its built-in **US opportunity ingestion is stronger**. Funding Autopilot currently emphasizes multi-region agent research and progression from a personal CV through eligibility, preparation, writing and review. |
| [Grantable](https://grantable.co/) | Organizational memory and donor/funder research, US IRS Form 990/federal funding sources, grant checklist, team-oriented writing/tracking | Useful for nonprofit organizational pipelines; Funding Autopilot focuses on the **individual academic researcher**, verified CV facts, degree timing, salary mechanisms and PI/host mobility. |
| [AI Job Search](https://github.com/MadsLorentzen/ai-job-search) | Source-specific job search, candidate onboarding, job-fit ranking, tailored materials and tracked outcomes | **Workflow inspiration rather than a research-grant competitor.** Funding Autopilot adapts the staged user journey with additional grants-specific eligibility, Host/PI and scientific preparation gates. |

## Sources

- PaperBreak: [product](https://paperbreak.ai/), [grant discovery and geographic coverage](https://www.paperbreak.ai/grant-discovery/), [user guide](https://paperbreak.ai/user-guide/).
- GrantWell: [GitHub README](https://github.com/The-Burnes-Center/AI4Impact-GrantWell).
- grant-finder: [GitHub README](https://github.com/openprose/grant-finder).
- Grantable: [product](https://grantable.co/), [its own October 2026 market comparison](https://grantable.co/guides/ai-grant-writing-tools) (self-published marketing, do not treat its third-party claims as independently tested).
- AI Job Search: [GitHub README](https://github.com/MadsLorentzen/ai-job-search).

## What the open-source source code actually supplies

The `Funding` repository has a portable Agent Skill, source registry, private profile and grant ledger, tests, a bounded UKRI RSS connector, structured gating and stage transitions, separate preparation and proposal scaffolding, and a conservative PDF inspection helper.

**Not implemented as a product:** an exhaustive worldwide funder database, a deployed document editor/web dashboard connected to live grants, automatic multi-country feed ingestion, background 12-month monitoring, PDF/DOCX generation by the CLI alone, or autonomous application submission. A capable AI host can do real web research and author outputs when actually configured. Mention this difference anywhere a comparison could otherwise be misleading.

## Distinctive research question

The project's differentiation is not "AI can find and write grants"; that is already widespread. It is an **evidence-conditioned, eligibility-first application workflow** that explicitly models the researcher's future career transitions and institutions, helps prepare the underlying research case before writing, and retains negative findings for future attempts.

This is a proposed product advantage, not demonstrated superiority, more grants won, an acceptance probability estimate, or proof of being first.
