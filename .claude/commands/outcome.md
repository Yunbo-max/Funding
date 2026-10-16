# /outcome — Record documented application progress

Read `skills/funding-autopilot/commands/05-outcome.md`. Treat `$ARGUMENTS` as the call key and requested status.

1. Run `python3 skills/funding-autopilot/scripts/workspace.py status` to identify a matching exact programme **round** and application route.
2. `drafting` and `draft_ready` mean **not submitted**. Do not infer submission from an AI-created PDF, a sent PI outreach email, or a deadline passing.
3. Only after the user explicitly confirms a real submission and provides a portal acknowledgement/reference (or a verified equivalent), run:
```bash
python3 skills/funding-autopilot/scripts/workspace.py outcome --key call-EXACT-KEY --to submitted --confirmed --receipt "<actual-reference>"
```
4. For awards, rejection or withdrawal record an actual written decision/reference and explicit user confirmation. Never auto-accept an award or infer rejection from silence.
5. Keep original submitted files, correspondence and feedback private. Produce follow-up **drafts only**, never automatically send email or change the student's employer/status.

Retain outcomes and eligibility failures as feedback for later rounds without inventing an award success rate.
