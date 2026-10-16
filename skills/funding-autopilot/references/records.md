# Structured records (v0.1)

All profile records are private by default. JSON examples in this repository are fictional. The local checker is a **conservative deterministic helper**, not a funder registry or policy oracle.

## Applicant profile

The `intake` command creates: `schema_version`, `cv_sha256`, `cv_file`, `extracted_text_file`, `text_characters`, `fields_verified` (false), `research_terms` (empty), `residence_country` (unknown), `phd_submitted_on` (unknown), `phd_awarded_on` (unknown), `host_confirmed` (false), `new_pi_confirmed` (false), `preferred_routes` (independent, new_pi), and `fact_evidence` (empty). The host agent populates these from the CV/user, preserves source pointers, and obtains confirmations. Unknown is never presumed true.

`phd_submitted_on` and `phd_awarded_on` are factual completed events, not target/expected dates. Record plans separately under `expected_phd_submission_on` or `expected_phd_award_on` so the checker cannot confuse them.

## Official call record

```json
{
  "id": "funder-program-2027-round1",
  "round": "2027-1",
  "title": "Illustrative research fellowship",
  "funder": "Example Foundation",
  "official_url": "https://example.org/fictional",
  "verified_at": "2026-10-16T14:00:00+00:00",
  "call_status": "open",
  "routes": ["independent", "new_pi"],
  "scope_terms": ["language models", "agent systems"],
  "salary_support": "yes",
  "requirements": {
    "requires_host": true,
    "requires_new_pi": false,
    "requires_phd_submission_by": "2027-02-18",
    "requires_phd_award_by": null,
    "eligible_residence_countries": ["GB"],
    "internal_deadline_status": "confirmed_none"
  },
  "deadlines": {
    "funder": "2027-02-18T23:59:00+00:00",
    "internal": null
  },
  "evidence": [
    {"field": "scope", "url": "https://example.org/fictional", "locator": "Section 1"},
    {"field": "eligibility", "url": "https://example.org/fictional", "locator": "Section 2"},
    {"field": "deadline", "url": "https://example.org/fictional", "locator": "Section 3"}
  ],
  "sections": [
    {"id": "summary", "max_words": 250, "required": true},
    {"id": "research_plan", "max_words": 1000, "required": true}
  ],
  "required_documents": ["cv", "host_letter"]
}
```

This is a **schema illustration, not an open real call**. A recorded timestamp and URL are evidence *metadata*, not automated verification of a source's honesty. A host must have retrieved and read the underlying official materials.

## Statuses from the helper

- `unverified`: missing/stale official page, checked-at timestamp or coverage of scope/eligibility/deadline evidence.
- `expired`: official call status closed or a confirmed applicable funder/internal deadline has passed.
- `ineligible`: verified hard conflict, including route not offered, residence excluded, or actual PhD milestone too late.
- `conditional`: verified call but missing actual applicant milestones, residence, host/new-PI confirmation, or internal deadline determination.
- `eligible`: all encoded verified gates pass; **subject to unencoded conditions and human review**.

A score is only a heuristic topical/practical fit index and does not estimate funding probability. A call may expose conditional status for one route and eligible status for another.

## Proposal/audit record

```json
{
  "call_id": "funder-program-2027-round1",
  "sections": {"summary": "Text...", "research_plan": "Text..."},
  "documents": ["cv", "host_letter"],
  "evidence_index": [{"id": "cv:p2", "kind": "cv", "locator": "CV p2", "verified": true}],
  "claims": [{"id": "c1", "text": "A CV-supported claim", "evidence_ids": ["cv:p2"]}],
  "approval": {"applicant": false, "pi": false, "host": false}
}
```

The audit checks section presence/approximate English word count, mandatory attachments, placeholder markers, claim pointers and call ID. It does not fact-check the prose, parse PDFs or establish final submission readiness. Human approval always remains required.

## v0.3 source-located CV facts

In addition to private `research_terms`, `preferences`, `expected_phd_submission_on` and `phd_awarded_on`, the profile records `fact_evidence`, an **append-only, conflict-checked** list. The AI host must generate a private JSON record of CV-derived facts after reading the uploaded file:

```json
{"cv_sha256": "<hash of the uploaded CV>", "facts": [
  {"id":"education-1","category":"education","claim":"[replace with CV-supported fact]","source_kind":"cv","locator":"CV page 1 / Education"},
  {"id":"publication-1","category":"publication","claim":"[replace with CV-supported fact]","source_kind":"cv","locator":"CV page 2 / Publications"}
]}
```

Run `workspace.py setup-facts --input-file private/cv-facts.json`; `setup-review` shows the evidence and user `setup-confirm` promotes proposed facts to `user_confirmed`. Re-running a fact ID with the same content is idempotent. A changed claim with an existing ID raises a conflict rather than rewriting source history. `source_kind` may be `cv`, `user` or `public`; no kind automatically certifies a claim. All source-located records stay in ignored private storage, not public GitHub.
