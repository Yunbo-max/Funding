# /rank — Check hard funding requirements before scoring

Read `skills/funding-autopilot/commands/03-rank.md` and `references/eligibility.md`. Use `$ARGUMENTS` to focus call or research area.

1. Load the reviewed private applicant profile and deduplicated ledger. Require that each proposed shortlist entry has the **specific official current round** and a checked date, not just a funder homepage.
2. Verify role independently for each path: individual fellow/applicant, independent PI, new PI-led project, hired postdoctoral researcher, prize applicant. A strong research fit never overrides missing legally necessary PI, host, career stage, nationality/residence/mobility, doctoral milestone, budget eligibility or internal approval.
3. Read official deadline **and** the new receiving institution's internal date; changing PI or institution invalidates any earlier internal deadline inference. Separate expected thesis submission from a completed PhD award.
4. Run:

```bash
python3 skills/funding-autopilot/scripts/workspace.py rank --limit 20
```

5. Present `eligible`, `conditional`, `unverified`, `ineligible`, and `expired` as separate categories. Each candidate has source links/locators, shortest true deadline, role, salary possibility and exact unresolved blocker. A fit score is only heuristic relevance, never an award probability.
6. Recommend applications worth time and explain both independence and the new-PI alternative. When user chooses one, use `/apply`. Store the chosen call's key and **route**; do not confuse two grants with the same programme title from different rounds.
