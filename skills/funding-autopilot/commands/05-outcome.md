# /outcome — Application tracking and learning

1. Load the private ledger and identify exactly one programme **round** and application route; if ambiguous, list the possibilities.
2. Separate stages: discovered, shortlisted, selected, drafting, draft_ready, submitted, under_review, awarded, rejected, withdrawn and archived. Treat `draft_ready` as **not submitted**. See `../references/pipeline-records.md` for transition rules.
3. For submitted or final outcomes, require user confirmation and an actual submission/decision reference; do not infer from an unrelated email snippet or a pasted grant portal page. Use `pipeline.py advance --confirm --evidence-ref <private-receipt-id>` only after explicit user approval.
4. Archive the submitted files as they actually existed, plus required annexes and host correspondence, to local ignored private storage. Do not reconstruct a submitted document from the latest draft and pretend it was the original.
5. A response from a grants office may show administrative review, a request for revision, or a decision. Record the *actual* wording and date. A rejection is evidence about this call, not a refutation of the researcher's ideas.
6. For a quiet submitted application, propose a concise follow-up email as a **draft**, based only on the recorded submission. Never auto-email. For declined/rejected proposals, record actual reviewer feedback and derive a versioned next-round repair plan; do not make acceptance statistics from a handful of cases.

Outcome: auditable status/history, actual receipts, and evidence for future applications.
