# BUILD-021 — VAT Extraction Quality & Evidence Validation (research)

## Baseline retained
The existing `synthetic50.py` / `paper50.py` exact-match benchmark is unchanged. Its fixture truth conventions do not establish real-document recall. Do not interpret its excellent synthetic VAT field precision/recall as production readiness.

## Independent synthetic evidence gate
`quality_cohort_v1.py` defines 14 manually specified, synthetic text-only invoice cases across explicit labels, consistent duplicates, missing VAT, non-VAT taxes, ambiguous conflicting amounts, unlabeled tax, and arithmetic contradictions. Each case has **two separate labels** specified prior to extraction:

- `semantic_truth`: what the fixture creator knows to be correct, even where the printed text is insufficient or contradictory.
- `supported_expected`: values the reviewed conservative parser can assert as **candidates** from the visible document alone, never tax conclusions.

The evaluator records correct supported candidates, safe abstentions, unsupported assertions, known-truth coverage misses, required review flags, provenance and violations of human-review/no-refund-claims constraints. Reports include aggregate numbers and synthetic case IDs only, never raw invoice text.

### Acceptance gate
- Exact supported-field assertions for the frozen fixture.
- No unsafe field assertions when supported_expected explicitly requires withholding.
- Required review flags present; human review required on all cases.
- No eligibility or recoverable amount claim.
- Independent false-positive and policy-violation injection tests fail the gate.

## Limitations / next gate
14 authored text examples do **not** represent PDF layouts, multilingual data distributions, real-world document recall, OCR errors, manual reviewer reliability, VAT law or claim feasibility. Arithmetic-conflict numbers remain **unverified candidate values** with a mandatory flag and may not be used to calculate refunds. Future independent research must measure realistic false negatives, abstention costs, time-to-review, and field-level error costs with permitted, properly governed evidence.

No tax advice, live processing, customer data, CI bypass, merge or deployment. `main` remains untouched until separate approval.
