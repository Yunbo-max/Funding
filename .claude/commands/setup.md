# /setup — Start a private Funding Autopilot profile

Use `skills/funding-autopilot/SKILL.md`, `commands/01-setup.md` and `references/intake-and-privacy.md`. The user's message arguments are `$ARGUMENTS`.

**The required input is a CV that the user has actually uploaded or made accessible as a local PDF, DOCX, TXT or MD.** A personal website cannot replace it. Do not pretend an inaccessible attachment was read.

1. Explain the privacy model before creating files in a public repository: all applicant data stay under `private/`, ignored by Git. Never push or paste the profile into GitHub issues. Verify a clean writable local runtime exists.
2. Read the CV and extract factual research topics, career stage, publications/projects and current employment. Present uncertainty, source pages and contradictions. Ask only for applicant preferences needed to decide next action: geography, independence vs new PI, salary requirement, research aim, expected/actual thesis submission, PhD award/start date. Never infer nationality, visas or host permission.
3. Run the CLI, selecting CV-supported research topic terms, e.g.:

```bash
python3 skills/funding-autopilot/scripts/workspace.py setup --cv "<local-cv>" --topics "machine learning,autonomous AI agents" --routes independent,new_pi --regions "UK,EU" --goal "independent research fellowship"
python3 skills/funding-autopilot/scripts/workspace.py setup-review
```

Include `--new-group` only if the applicant wants to leave the current group, `--salary` only if their personal income is part of the objective, and `--expected-thesis YYYY-MM-DD` only for a **planned** thesis submission. A future planned milestone cannot be recorded as an actual submission or award.

4. Present the extracted profile and important open questions. **Do not** automatically run `setup-confirm`. Once the user explicitly approves the facts, run:

```bash
python3 skills/funding-autopilot/scripts/workspace.py setup-confirm --confirm-reviewed
```

Never overwrite an existing profile without an explicit replacement decision. The CLI's `--replace` is destructive, not a default. Resume with `/search`.

### Existing profile update

If the applicant wants to change fields but the uploaded CV and saved profile already exist, use `/setup-update` or `workspace.py setup-update --topics "..." --regions "..." --salary yes|no --new-group yes|no`. Preserve the CV hash, prior grant ledger and other evidence; reset profile confirmation and request a fresh user review. Never treat an expected future PhD milestone as a completed one.
