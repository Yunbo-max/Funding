# /prepare — Separate funding strategy development

**Entry:** /match produced an officially verified current-round call; the applicant selects its exact key and either independent or new_pi route.

1. Recheck funder and receiving institution rules, internal deadline, degree milestone, role, salary eligibility and required form fields. Read [preparation contract](../references/preparation.md).
2. Run **python3 skills/funding-autopilot/scripts/workspace.py prepare --key call-EXACT-KEY --route independent** (or new_pi). This creates a private preparation.md, preparation.json, requirements checklist and, for new_pi, an **unsent** outreach draft. Stage becomes preparing.
3. The AI host actually develops a grant strategy: original research question or evidence-backed impact case, distinctive approach, strongest prior work/baselines, evaluation, timeline and feasibility. Connect each proposed claim to reviewed CV evidence IDs and each official form field to a substantive outline. Record PI/Host and cost assumptions, supporting letters and unresolved approvals.
4. Present the preparation plan to the applicant, revise it as needed, and explain why this grant/Host/PI route is appropriate. Do not mark host consent or a budget allocation confirmed without real evidence.
5. Once the applicant has explicitly reviewed and accepted the actual plan, run **workspace.py prepare-complete --key call-EXACT-KEY --confirm-reviewed**. The command enforces source identity, sourced CV facts and required outlines. It cannot prove originality or eligibility on its own.
6. Only after stage prepared should /apply draft the actual research proposal. Conditional new-PI routes can still be exploratory, but cannot be submission-ready.

Never submit applications, send PI emails, commit private applicant files, or start background jobs in this phase.
