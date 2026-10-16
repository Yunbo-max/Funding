# Install Funding Autopilot

## Agent Skills-compatible hosts

Copy the **entire** `skills/funding-autopilot/` directory (including `references/`, `assets/`, and `scripts/`) to a skills directory recognized by your host. Do not copy only SKILL.md, because its procedures refer to additional local files.

For a local Codex-style personal setup:

```bash
git clone https://github.com/Yunbo-max/Funding.git
mkdir -p ~/.agents/skills
cp -R Funding/skills/funding-autopilot ~/.agents/skills/
```

For a project-scoped skills setup, copy the same directory to the host's supported project skills location (often `.agents/skills/`). Confirm your host supports Agent Skills discovery and load a new session if necessary. Installation of a repository does not itself grant live web, PDF-reading, GitHub writing, or scheduling permissions.

## Optional document parsers and testing

```bash
cd Funding
python3 -m pip install -e '.[documents]'
python3 -m unittest discover -s tests -v
```

Only PDF/DOCX intake needs these optional libraries; TXT/MD intake and the eligibility/audit checks use Python's standard library. The **AI host**, not the Python checker, must read official websites and draft substantive proposal prose.

Keep personal inputs and outputs under `private/` (ignored by Git). Do not publish private research pitches or contact details. The repo intentionally contains no GitHub workflow and does not activate background monitoring.

## Verify the installation

1. Supply an actual CV attachment to the host.
2. Request funding discovery and the exact official sources/eligibility gates.
3. Confirm that without a CV, personal matching stops; without official call verification, it does not assert eligibility.
4. Choose a real verified call, run `prepare` for a blank application-specific template and ask the agent to fill its sections with auditable evidence.
5. Run `audit` and complete human/host review before any submission.

## Stateful pipeline (v0.2)

After the host has read official funder sources and written `private/discovered-calls.json`:

```bash
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json ingest --input private/discovered-calls.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json batch --limit 10
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json rank --profile private/profile.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json report --out private/funding-report.html
```

To advance an application stage safely:

```bash
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json advance --key call-EXACT-KEY --to shortlisted
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json advance --key call-EXACT-KEY --to selected --route independent
```

`submitted` and decision statuses additionally require an explicit human confirmation and receipt reference, as specified in [the pipeline contract](../skills/funding-autopilot/references/pipeline-records.md). Do not use these commands to impersonate a human approval. The `--state` file and HTML `--out` MUST resolve inside a directory literally called `private`.

Optional PDF mechanical checks, after producing a real application PDF:

```bash
python3 skills/funding-autopilot/scripts/verify_grant_pdf.py --pdf private/application.pdf --max-pages 5 --must-contain "Research"
```

The actual maximum page count and required field wording must come from the selected official call. Passing this script **never replaces visually inspecting the rendered PDF**. The `[documents]` extra includes `pypdf`.

Run the full local unit suite with `python3 -m unittest discover -s tests -v`. The six to eight phases described in `skills/funding-autopilot/commands/` are agent instructions, not an automatically installed scheduler.

## Optional UKRI RSS discovery

```bash
python3 skills/funding-autopilot/sources/ukri_rss.py search --query "machine learning" --limit 20
```

This contacts UKRI's public RSS URL only when the host permits HTTPS. It searches recently syndicated calls, not the full UKRI funding catalogue; never treat results as verified eligibility. For offline tests use the optional `--xml-file` argument with local fixtures. See [source documentation](../skills/funding-autopilot/sources/README.md).

## User-facing Claude Code commands and local workbench (v0.3)

Clone this repository, open its root as the working directory in Claude Code, then type `/setup`, `/search`, `/rank`, `/apply`, `/outcome` or `/status`. The instructions for these commands are in `.claude/commands/`. They call the same Skill and Python helper; no separate plugin installation is needed in a standard Claude Code project that supports repository commands.

For any other Agent Skills host, copy `skills/funding-autopilot/` to its recognized skills directory and request the workflow in a chat. The slash commands are Claude Code-specific; they do not automatically appear as slash commands in ChatGPT.

A researcher can change research areas or preferences **without uploading the same CV again**:

```bash
python3 skills/funding-autopilot/scripts/workspace.py setup-update --topics "machine learning,agent safety" --salary yes --new-group yes
python3 skills/funding-autopilot/scripts/workspace.py setup-review
# Only after explicit applicant approval:
python3 skills/funding-autopilot/scripts/workspace.py setup-confirm --confirm-reviewed
```

Read [the user walkthrough](USER-WORKFLOW.md) for the entire on-demand sequence and safety model. The optional `[documents]` dependency supplies PDF/DOCX CV parsers, but full PDF/DOCX proposal generation uses the authorized AI host's artifact tools. Local tests do not establish live website reachability or platform account access.

## v0.4 — Match, Prepare, Apply

In a supported Claude Code project, the six-stage workflow uses `/setup`, `/search`, `/match`, `/prepare`, `/apply`, and `/outcome`. `/rank` remains compatible as an alias for `/match`.

With the real scheme and CV facts reviewed, first **prepare a grant strategy**:

```bash
python3 skills/funding-autopilot/scripts/workspace.py match
python3 skills/funding-autopilot/scripts/workspace.py prepare --key call-VERIFIED-KEY --route independent
```

The AI host must write real research strategy, section outlines and CV evidence IDs into `private/applications/<key>/<route>/preparation.json` and `preparation.md`, for the user's actual review. Only after the user confirms:

```bash
python3 skills/funding-autopilot/scripts/workspace.py prepare-complete --key call-VERIFIED-KEY --confirm-reviewed
python3 skills/funding-autopilot/scripts/workspace.py apply --key call-VERIFIED-KEY
```

`apply` starts writing the complete proposal from the reviewed plan. Its CLI only scaffolds the specific sections; the agent handles substantive writing and critical review. Neither status grants permission to submit automatically. [Preparation contract](PREPARATION-CONTRACT.md).

## A year-long plan (agent-assisted)

In Claude Code, use `/year-plan` after `/setup` to create a private 12-month readiness document from approved CV facts and verified funding rounds. This is a **Claude Code AI-host command**, not a new workspace.py CLI subcommand. The public twelve-month SVG illustrates overlapping work, not actual funder deadlines. No monitoring or future reminders are started.
