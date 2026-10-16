# Funding Autopilot — English editorial redesign

Date: 2026-10-16.

## Delivered

- Updated the main README to English-only and translated the proposed headline to: **"There are no researchers who cannot secure funding—only those who are not ready when opportunity arrives."** It is identified as a motivational statement, **not** a grant-success guarantee.
- Replaced all four graphics with original, pure-SVG editorial illustrations: `assets/hero.svg`, `assets/workflow.svg`, `assets/yearly-roadmap.svg` and `assets/proposal-strategies.svg`.
- Adopted a print-journal / Swiss editorial aesthetic with warm paper (#F5F2EA), forest green ink, brick red detail, large Georgia headlines, thin black rules and generous whitespace. No neon-glow, gradients, chat bubbles, robots, stock photos, third-party fonts or fake application screenshot claims.
- Kept the functionality documentation, sourced competitor comparison, global coverage limitations and example Input → Output unchanged in substance. Updated brand identity guidance and deleted the now-unwanted Chinese translation.
- Updated source regression tests with English-only and editorial SVG constraints. Existing private CV and application data were never accessed or committed.

## Verification conducted

- Checked source records by authenticated GitHub readback.
- In-process static structural checks on all four SVGs: nested tag balancing, raw ampersands, file envelope, no external image/gradient/filters, and correct editorial palette.
- Checked README for Chinese characters, exact English slogan, and existing relative references; all checked repository-relative links resolved. Confirmed there are still **zero GitHub Actions / workflows**.

## Limits

- No executable render/browser screenshot was available for the GitHub-hosted SVGs through the current linked source tools; source-level checking does not guarantee identical text layout on all operating systems.
- Newly added Python tests have been committed but **not executed in a clean local clone** during this turn.
- No changes to grant eligibility, source adapters, user CV data, automated jobs, email sending or application submissions.
