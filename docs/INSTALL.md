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
