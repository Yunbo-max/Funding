# CV intake and privacy

## Require the actual CV

A file the user uploads is the starting source. It may be PDF, DOCX, MD or TXT. Extract full text (tables and multi-column order can be wrong); note any inaccessible pages or extraction errors. A homepage, ORCID, publication list or past Chat conversation can *supplement* the CV but does not replace the required uploaded document. If there is no file, ask for CV before personalized research.

Create an evidence ledger: `profile_fact_id | field | exact wording or faithful paraphrase | CV page/heading | status(observed/user-confirmed/inferred/unknown) | checked_at`. Split authoritative CV facts from user-provided changes, e.g. an upcoming thesis submission date. Do not turn planned events into achievements.

## Information useful for matching

- Current affiliation/employment/registration, dates; expected departure and available start date.
- Doctoral programme, **actual thesis submission date**, expected submission date, viva, degree award date (each separate).
- Research areas, methodological competence, publications and contribution descriptions actually supported.
- Independence preference: own PI, mentorship via a new PI, another institution, postdoc salary vs project budget.
- Employment, residence, nationality, disability, caregiving and immigration information **only if a particular opportunity requires it**. These can be sensitive: ask only when required, let applicant withhold, and mark the call conditional if unresolved.
- Host willingness/letter, departmental approval, employment contract, cost matching, eligible institution status.

Do not infer citizenship, work authorization, eligibility to receive salary, NHS affiliation, professorial status, PhD completion or existing outside collaboration from university affiliation alone.

## Privacy and output

Never commit CV, extracted CV text, profiles, proposals, email addresses, salary information or collaborator drafts to a public repo without affirmative separate permission. Default output directory is `private/`, already git-ignored. Do not auto-send CV contents to external portals. Logs in the public repo may contain only source-code revisions, aggregate test outcomes and non-identifying operational notes.

If the user corrects a CV field, keep the CV original observation and add an explicit user-confirmed correction. If data is stale, ask to confirm only what materially changes eligibility or the chosen application.
