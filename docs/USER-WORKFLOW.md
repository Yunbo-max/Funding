# Funding Autopilot: user workflow

The goal is to offer the same **setup → search → rank → apply → outcome** user journey that makes [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) practical, while enforcing real academic eligibility and host-institution rules.

## 1. Install and open

```bash
git clone https://github.com/Yunbo-max/Funding.git
cd Funding
python3 -m pip install -e '.[documents]'  # optional for PDF and DOCX CVs
```

If using **Claude Code**, open the repository as the working directory and issue `/setup`. This repository now contains native `.claude/commands/` instructions. On a generic Agent Skills host, copy `skills/funding-autopilot/` into the host's recognized skills folder and request the same workflow in natural language. The local CLI works without Claude Code but cannot write substantive grant narrative or search non-UKRI portals without a host agent.

## 2. Setup (CV first, private by default)

Upload a CV (PDF/DOCX/TXT/MD) to the agent host, or pass the local path:

```bash
python3 skills/funding-autopilot/scripts/workspace.py setup \
  --cv "/absolute/path/to/cv.pdf" \
  --topics "machine learning,autonomous agents,verification" \
  --regions "UK,EU" \
  --routes "independent,new_pi" \
  --goal "early-career independent funding" \
  --new-group --salary \
  --expected-thesis 2026-11-25
python3 skills/funding-autopilot/scripts/workspace.py setup-review
```

The last line displays claims to check, but does not certify them. If and only if the user has reviewed and approved the actual facts:

```bash
python3 skills/funding-autopilot/scripts/workspace.py setup-confirm --confirm-reviewed
```

All personal data go into `private/profile.json` and `private/profile.cv.txt` and are ignored by Git; they are **not** put in the public open-source repository. A future thesis submission stays a future expectation until it actually happens.

## 3. Search

With an actual supported host connection for public HTTPS, the UKRI recent-opportunities RSS feed can be searched:

```bash
python3 skills/funding-autopilot/scripts/workspace.py search --query "AI,research fellowship" --limit 20
```

The host's AI browsing can also discover global/other funder leads and write a private JSON array:

```json
[
  {
    "id": "example-official-call-id",
    "funder": "Example Funder",
    "round": "unverified",
    "title": "Actual title copied from an official funder page",
    "official_url": "https://www.example.org/call",
    "discovered_via": "official-page-search"
  }
]
```

```bash
python3 skills/funding-autopilot/scripts/workspace.py search --input-file private/discovered-calls.json
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json batch --limit 10
```

The JSON block above is **structural illustration only**; it is not a live grant. Do not treat RSS links or search summaries as proof of who can apply.

## 4. Verify then rank

The agent opens the exact current scheme guidance, derives a full structured call record (including sources and specific current round), and promotes the matching lead:

```bash
python3 skills/funding-autopilot/scripts/workspace.py verify \
  --key call-DISCOVERY-KEY --call-file private/official-call.json
python3 skills/funding-autopilot/scripts/workspace.py rank --limit 20
```

A key changes if `round` changes from `unverified` to the real cycle. **Use the new returned key** for later actions. Check (i) applicant vs PI role, (ii) completed vs expected PhD date, (iii) salary and institution, and (iv) both funder and new-host internal deadlines. `conditional` is not `eligible`; it identifies unresolved approvals or facts.

## 5. Write and review a proposal

```bash
python3 skills/funding-autopilot/scripts/workspace.py apply \
  --key call-VERIFIED-KEY --route independent
```

This creates a private call-specific scaffold, compliance checklist and application manifest. On `new_pi`, it also creates an **unsent PI outreach draft**. Ask the agent to **actually compose** complete proposal sections, not just return the scaffold. Then request independent reviewer passes, exact funder field limits, actual document rendering and audited `proposal.json`.

Only after the applicant explicitly confirms all required approvals and the call-specific structured audit passes, `ready --key ... --proposal-json ... --confirm-reviewed` records `draft_ready`. It does **not** submit. `submitted` and grant decisions require external evidence/receipt.

## 6. Track results

```bash
python3 skills/funding-autopilot/scripts/workspace.py status
python3 skills/funding-autopilot/scripts/pipeline.py --state private/ledger.json \
  report --out private/funding-report.html
```

Save actual submission outcomes only with applicant approval and receipt; the dashboard stays private. No automatic background search, GitHub Actions or external messaging is installed. A model or Skill alone cannot schedule autonomous repeated checks.

## Clear limitations

- **Implemented and runnable locally:** upload-path CV intake, private reviewed profile, UKRI RSS/search-import lead intake, round promotion, route-specific eligibility checks, call-shaped draft scaffolding, bounded persistent tracking and structure audit.
- **Requires an AI host with real online research and writing tools:** searching other official portals, reviewing full guidance, producing source-grounded proposal prose, independent content review, generating editable documents.
- **Requires an applicant/institution:** PI or Host acceptance, internal deadlines, budgets, signature and actual submission.
- The offline sample tests use fictional people and funding calls. Never advertise test examples as live funding.
