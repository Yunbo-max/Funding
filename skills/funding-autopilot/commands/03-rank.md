# /rank — Eligibility-first, bounded screening

1. Require a source-backed CV profile and load its version once. Retrieve a compact work batch using `pipeline.py --state private/ledger.json batch --limit 10`, not the entire lifetime ledger.
2. For each selected call, fetch authoritative current-round guidance and apply `../references/eligibility.md`. Independent PI, individual fellow, collaborator/new PI and postdoc employment are **separate routes**.
3. Enforce hard gates before topical ranking: applicant type, degree milestone at the exact measurement date, PI appointment, institution host, residency or mobility rules where applicable, salary/cost eligibility, both funder and host-internal dates, scheme research scope and any institutional quota.
4. Run `pipeline.py --state private/ledger.json rank --profile private/profile.json` on the vetted full-call JSON. The Python status remains conservative and the fit score is **not** acceptance probability. If the profile is unreviewed or official evidence is missing, show conditional/unverified, not eligible.
5. Compare verified eligible routes by research fit, career independence, personal salary coverage, host feasibility and preparation time. Explain subjective recommendations separately from hard rules. Maintain conditional and ineligible lists with blockers.
6. Mark excluded and postponed leads in state without deleting them. Reopen past leads only after a new official round/source check. Do not infer undocumented deadlines.

Outcome: a few actionable, source-cited routes plus distinct missing permissions, host contacts and the shortest applicable deadline. User chooses which verified route to enter `prepare`; preparation is required before Apply.
