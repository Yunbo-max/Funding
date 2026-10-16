# /prepare — Research strategy before proposal drafting

Read **skills/funding-autopilot/commands/04-prepare.md** and **skills/funding-autopilot/references/preparation.md**. Arguments may identify a call key and independent/new_pi route.

1. Confirm the intended funding call and route were checked against the exact official current-round guidance and institutional deadline. The researcher's uploaded CV has been reviewed.
2. Run **python3 skills/funding-autopilot/scripts/workspace.py prepare --key call-EXACT-KEY --route independent** (or new_pi). It creates the private planning files and stage preparing, not drafting.
3. Read preparation.md, preparation.json and requirements.md. **Actually write the scientific and administrative strategy**: choose the problem, distinct method, strongest alternatives, feasible evaluation, milestones, CV-grounded fact IDs, PI/Host approach, salary and budget mechanism, supporting documents and a purpose-built outline for each required funder field. Flag missing evidence and approvals rather than inventing them.
4. Discuss alternative framings, PI choices or required confirmations with the applicant. A template containing placeholders is not completed preparation.
5. After the applicant explicitly approves the populated plan, run **python3 skills/funding-autopilot/scripts/workspace.py prepare-complete --key call-EXACT-KEY --confirm-reviewed**. Only if this passes should you offer /apply.

This stage never sends letters or submits an application. Keep CV, strategy, budgets, and PI outreach under ignored private/ paths.
