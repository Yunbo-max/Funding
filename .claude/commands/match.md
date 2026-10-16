# /match — Verify funding fit and eligibility

This is the canonical name for legacy /rank; both run the same underlying eligibility checker.

1. Read the user-confirmed CV profile, official current-round funding guidance and receiving institution internal deadline. Check independent and new_pi applicant routes separately.
2. Enforce PI authority, thesis submitted vs PhD awarded milestones, Host approvals, permitted salary/costing and geographic or career-stage requirements **before** research fit scoring.
3. Run **python3 skills/funding-autopilot/scripts/workspace.py match --limit 20**. Report eligible, conditional, unverified, ineligible and expired calls separately, with exact source locators and the shortest applicable deadline.
4. Let the applicant choose a call and route. **Next: /prepare** to build the research strategy, CV-evidence map, PI/Host plan and budget before any proposal drafting.

Do not treat a strong topic match as an eligibility pass or skip directly to /apply.
