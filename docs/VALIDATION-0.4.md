# Funding Autopilot v0.4 — validation record

Date: 2026-10-16. This update was published through direct GitHub source commits with exact expected-parent checks and subsequent file/tree readback. The two SVG images are source assets for the GitHub README; they are not real application screenshots.

## What changed

- New pipeline application stages: preparing and prepared.
- New workspace commands: match (legacy rank alias), prepare, prepare-complete. Apply now requires the applicant-reviewed prepared packet.
- Preparation files stay in ignored private/ paths; source identity, user-confirmed CV fact IDs, proposal section outlines and explicit applicant confirmation are mandatory.
- Source-level test files were updated to cover direct stage bypasses, CV fact references, absent section outlines, conditional new PI, user confirmation and route transitions.

## Not validated in this turn

- The full Python regression suite has **not** been run end to end on a clean checkout in this turn; GitHub source tools do not execute code.
- No actual funder/PI approval, completed proposal writing against a live scheme, web UI screenshot, PDF rendering or real application submission was tested.
- The previous v0.3 test numbers remain historical results, not evidence that the new v0.4 test suite passes.

## Recommended local checks

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile skills/funding-autopilot/scripts/workspace.py skills/funding-autopilot/scripts/pipeline.py
```

The supplied tests use fictional CVs and funding calls, not genuine grant availability; even a passing test suite is not evidence of real-life grant acceptance.
