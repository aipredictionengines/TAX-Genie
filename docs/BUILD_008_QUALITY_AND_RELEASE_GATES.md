# BUILD-008: quality and security gate — NOT production ready

## Benchmark cohorts (synthetic only)
- Original frozen 50 retained without ground-truth modifications.
- First independent holdout 50 retained; expected VAT recall is now 0.75 (30 TP, 10 FN, 0 FP, 10 TN).
- Both are regression checks. Because the parser has been modified in response to holdout failures, neither cohort provides an untouched prospective quality estimate.
- No representative real invoice sample has been tested, and OCR remains disabled.
- Quality gate remains BLOCKED because holdout recall is below 0.90 and no untouched prospective holdout has passed.

## Blocking professional release gates
SECURITY: BLOCKED — independent audit, protected file-parser execution, malware controls, auth/token lifecycle, tenant boundary tests, rate limiting, HTTPS and managed keys not verified.
PRIVACY: BLOCKED — DPIA determination, lawful-basis review, consent documentation if appropriate, DPA, retention, backups and data subject controls not externally validated.
LEGAL: BLOCKED — DE→FR EU VAT applicability and country expense rules not approved by qualified specialist; PR #2 remains draft.
REAL_PAPER_50: BLOCKED — consented documents, secure environment and independently frozen human labels unavailable.
PRODUCTION: BLOCKED — no external taxpayer traffic permitted.

## Release ordering
1. CI + code review for this change.
2. New prospective synthetic holdout created independently before parser iteration.
3. Independent security assessment and privacy counsel review, remediate findings.
4. Qualified France/Germany cross-border VAT reviewer signs off sourced rules.
5. Approved secure environment, anonymized/consented Real PAPER 50 with independent labeling.
6. Only then consider a restricted pilot.
