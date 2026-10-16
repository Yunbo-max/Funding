# /setup-update — Edit a saved applicant profile without reuploading CV

Use `skills/funding-autopilot/commands/01-setup.md` and `references/intake-and-privacy.md`. `$ARGUMENTS` specifies which researcher preferences or facts changed.

1. Check a real uploaded-CV-backed `private/profile.json` exists. If absent, ask for `/setup`; do not fabricate the CV.
2. Identify only changed fields and obtain applicant confirmation for factual doctoral milestones, employment and PI status. Treat the original CV/source pointers as immutable observations and preserve call history.
3. Run `python3 skills/funding-autopilot/scripts/workspace.py setup-update --topics "..." --regions "UK,EU" --salary yes --new-group yes` using **only** options the user actually changed. Additional options include `--routes`, `--goal`, `--residence`, `--expected-thesis`, `--submitted-thesis`, `--phd-awarded`, and `--start-after`.
4. Run `workspace.py setup-review`, present the changes and contradictions, then only after explicit user confirmation run `workspace.py setup-confirm --confirm-reviewed`.
5. Re-run `/rank` for any open opportunities because the new CV-derived preferences may invalidate earlier eligibility, institute assumptions or research-topic fit.

CVs and profiles remain under ignored `private/`; none is published or emailed.
