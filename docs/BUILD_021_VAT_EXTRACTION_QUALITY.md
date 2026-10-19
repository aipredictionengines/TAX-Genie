# BUILD-021 — VAT Extraction Quality & Evidence Validation (research)

## Baseline retained
The existing `synthetic50.py` / `paper50.py` exact-match benchmark is unchanged. Its fixture truth conventions do not establish real-document recall. Do not interpret its excellent synthetic VAT field precision/recall as production readiness.

## Authored synthetic evidence gate (not externally validated)
`quality_cohort_v1.py` defines 14 manually specified, synthetic text-only invoice cases across explicit labels, consistent duplicates, missing VAT, non-VAT taxes, ambiguous conflicting amounts, unlabeled tax, and arithmetic contradictions. Each case has **two separate labels** specified prior to extraction:

- `semantic_truth`: what the fixture creator knows to be correct, even where the printed text is insufficient or contradictory.
- `supported_expected`: values the reviewed conservative parser can assert as **candidates** from the visible document alone, never tax conclusions.

The evaluator records supported candidates, **separately** counts (a) absences for which semantic truth has no VAT field and (b) safe abstentions despite a known synthetic VAT value, unsupported assertions, known-truth coverage misses, required review flags, **source-line provenance matched against the source line content**, and violations of human-review/no-refund-claims constraints. Reports include aggregate numbers and synthetic case IDs only, never raw invoice text.

### Auditable synthetic-only score definitions

On the frozen 14 authored fixtures, the intended denominator is 98 field-slots (14 cases × 7 supported fields). There are 94 fields with authored semantic truth, 90 safely supported field expectations, four correct abstentions on genuinely absent truth, and four safe abstentions on known-but-not-verifiable VAT amounts. Therefore 100% supported-candidate accuracy can coexist with 90/94 = 95.74% semantic exact coverage. Neither score measures external-document extraction accuracy or production readiness.

Provenance validation checks that every returned labeled-regex candidate points to an in-range source line and that the line actually matches the candidate field and value. This is a regression consistency check using the same parser label patterns, **not independent proof of field truth**.

These labels and scores are authored by the same development effort; an independent human review of the fixture specification remains necessary. An evaluator pass does not represent independent audit acceptance.

### Acceptance gate
- Exact supported-field assertions for the frozen fixture.
- No unsafe field assertions when supported_expected explicitly requires withholding.
- Required review flags present; human review required on all cases.
- No eligibility or recoverable amount claim.
- False-positive, bad-provenance, wrong-value, missing-flag and policy-violation injection tests fail the gate.

## Limitations / next gate
14 authored text examples do **not** represent PDF layouts, multilingual data distributions, real-world document recall, OCR errors, manual reviewer reliability, VAT law or claim feasibility. Arithmetic-conflict numbers remain **unverified candidate values** with a mandatory flag and may not be used to calculate refunds. Future independent research must measure realistic false negatives, abstention costs, time-to-review, and field-level error costs with permitted, properly governed evidence.

No tax advice, live processing, customer data, CI bypass, merge or deployment. `main` remains untouched until separate approval.
