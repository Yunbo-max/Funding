# /apply — Write and review a real application from the completed Prepare packet

**Do not skip /prepare.** This command requires a user-reviewed prepared research strategy for the exact call and route; **workspace.py apply** enforces the stage.

1. Read the confirmed private preparation.json/preparation.md, actual official current-round form and requirements, confirmed CV facts and relevant source papers. If preparation is still incomplete, return to /prepare.
2. Run **python3 skills/funding-autopilot/scripts/workspace.py apply --key call-EXACT-KEY** (route is inherited from Prepare). The CLI creates only the call-shaped proposal.md scaffold and moves the application to drafting. It does not generate substantive grant prose.
3. The AI host **must draft complete real sections** using the exact scheme section IDs, word limits, evaluation criteria and user-approved research strategy: question, novelty, objective, method, comparators, work packages, milestones, impact, Host/PI, salary/budget, ethics/data and risk as required. Create a private proposal.json with actual claims, verified evidence IDs, required documents and approvals.
4. Run independent **eligibility/compliance** and **scientific-merit** reviews. Revise specific deficiencies. Validate word/page limits, attachments and evidence using funding.py audit, then render/read actual documents using available DOCX/PDF/LaTeX tools when requested.
5. Leave unverified partner, research result or budget facts as explicit missing evidence. A conditional opportunity may produce an exploratory concept, not a submission-ready application.
6. Only after real applicant/PI/Host approvals and a passing scheme-structured audit may **workspace.py ready --key call-EXACT-KEY --proposal-json private/actual-proposal.json --confirm-reviewed** move to draft_ready. This **does not submit**.
7. Real submission requires explicit user authorization and a portal receipt, recorded later through /outcome. Never auto-send PI outreach, upload the CV publicly or claim funding was obtained.

**Deliverable:** source-grounded editable application draft plus compliance checklist, evidence map and review issues; otherwise report honestly what remains blocked.
