# /report and optional /inbox — Visibility without silent writes

## /report

Run `pipeline.py --state private/ledger.json report --out private/funding-report.html` to generate a self-contained offline HTML report; browser access is not needed. It displays current stages, route-specific eligibility, deadlines and official URLs. It does not change the ledger, fabricate statistics or expose data to remote analytics. **The report contains private application metadata and must stay private.** Empty fields display as unknown.

## /inbox (explicit opt-in only)

Use the actual connected mail service only if the user requests it. Restrict the search to named active funder/host applications and a bounded date range. Read full messages, not snippets alone. Match to exact funder, round and applicant; never equate "your application was received" with "award granted." Cite every proposed update to the actual email and show conflicts/unmatched mail.

**Approval barrier:** display proposed changes first. Do not change the ledger, send mail, accept an award, withdraw an application, or forward sensitive material without explicit user confirmation. Keep receipt IDs private. If the mail connector is unavailable, do not try workarounds that bypass the account's permissions.

Outcomes and deadlines may be monitored only using a real host-supported scheduler separately authorized by the user; no repo workflow or read-only command activates a background process.
