# Funding Autopilot v0.3 local validation (2026-10-16)

## Scope

These are **real local commands and assertions**, but the new workspace integration tests used temporary fictional CVs/calls and local **test doubles** matching the existing `funding.py` and `pipeline.py` public interfaces. This is a validation of the new orchestration behavior, **not** an assertion that real official grant pages, external submission portals, or the entire existing test suite were exercised. No personal applicant data was used.

## Observed local checks

- `python -m py_compile skills/funding-autopilot/scripts/workspace.py`: exit 0.
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_workspace.py' -q` in the isolated test harness: **16 tests passed**, exit 0.
- Explicit CLI smoke commands exercised `workspace.py setup`, `setup-review`, `setup-confirm`, `search --input-file` and `status` using fictional input and verified the output JSON and private profile path; exit 0.
- GitHub source and test blob SHA readbacks were compared with exact locally tested files during publication.

Covered: source-located private CV fact import, contradictions, idempotent fact deduplication, applicant confirmation, CV required, profile review gating, preferences/new-group/salary, incremental no-reupload updates, no silent profile overwrite, future PhD dates rejected, official round migration, repeat-feed dedup, conditional vs eligible role assessment, source/host mismatch, private call-specific draft creation/idempotence, conditional PI only concept, structure/approval ready review, submission receipt and rejection of unverified discovery leads.

## Known gaps

- The v0.3 test harness used controlled substitutes for `funding.py` and `pipeline.py`. Their existing repository tests remain published but were **not run in the same local integration**. A clean full checkout is needed for one combined full-suite test.
- The connected cloud GitHub tools support source edits/readback, not remote code execution. Source publication does not certify deployment to a personal Claude or ChatGPT installation.
- No actual UKRI RSS HTTP fetch, European grant API, global grant crawler or funder portal application was run. UKRI parsing itself had prior offline fixture tests.
- `workspace.py apply` **creates a scaffold only**; a real AI host with user-provided CV and verified current funder guidance must write and review complete proposal prose and supported editable documents.
- Nothing submits applications, sends emails, accepts funding, makes employment offers or sets up background monitoring.
