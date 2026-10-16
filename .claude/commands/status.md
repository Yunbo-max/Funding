# /status — Show the private funding pipeline

Read `skills/funding-autopilot/references/pipeline-records.md`. Run:

```bash
python3 skills/funding-autopilot/scripts/workspace.py status
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json report --out private/funding-report.html
```

Report known applications by official programme/round, stage, role, eligibility and next action. Flag unknown internal deadlines and stale official source records. Link or open the local **private** HTML dashboard only for the applicant; never commit or publish it. Missing profile → offer `/setup`. Empty leads → offer `/search`. No live scheduler is activated by these commands.
