# BUILD-021 — Independent fixture review protocol (PENDING)

**Status:** packet preparation only. No independent reviewer has been appointed,
no review evidence has been received, and no independent acceptance may be claimed.
This is an internal preparation step, **not** an independent audit.

## What is frozen and in scope

- Repository: `proofandsignal/TAX-Genie`, PR #21; review a **specific head commit**.
- Synthetic text dataset: `tax_genie/quality_cohort_v1.py`, 14 cases.
- Initial fixture file Git blob SHA when packet was created:
  `420848af241ec1e28dba283ed1c445daa6404d30`. Revalidate it before any review.
- Existing PAPER 50 benchmark remains unchanged and separately interpreted.
- Generate the **blind source-only** review packet:
  `python -m tax_genie.fixture_review_packet > build021-blind-packet.json`
- Compare the packet's `packet_sha256` against the same frozen packet after review.
  The digest detects changes to the exported source-only packet; it proves
  neither the truth of labels nor the independence of a reviewer.

The packet exposes synthetic case IDs, text and a field-name rubric **only**.
It intentionally hides `semantic_truth`, `supported_expected`, expected
review flags, prior parser output and expected quality scores. Because
the repository is public, the reviewer must receive only the blind packet
until their **initial judgments** are recorded, not browse its answer-key files.

## Independent reviewer assignment (human)

Reviewer must be a different person from the author of the fixture and
quality evaluator and have appropriate VAT/invoice-document domain experience.
Ask them to review only the synthetic packet. Do not share client files or
credentials. For **each** case, record:

1. Whether each of the seven fields is **safely supported by source text**
   (candidate value + line number) or **ABSTAIN** (with reason).
2. Conflict/missing/arithmetic warning flags that must be raised, including
   exact evidence lines for any conflict.
3. Whether source content is insufficient to determine semantic truth and
   which scenario assumptions would be necessary. **Do not guess** hidden
   truth in contradictory or unlabeled scenarios.
4. Errors, alternate valid readings, unsafe tax interpretations, and any
   ambiguous label definitions.

Before viewing author labels, reviewer should finalize an initial record
including packet digest, case IDs, decisions, reviewer role (no identity
details in public repository), review date, rubric version, and unresolved
issues. Store signed/private reviewer evidence outside the public repo.

## Adjudication / evidence gate

Only **after** independent first-pass review:
- Compare the reviewer decisions with `supported_expected` and
  `required_review_flags`, reporting per-case disagreements and rationale.
- Treat `semantic_truth` as **author-supplied scenario assumptions** for
  known-but-unobservable amounts: reviewer cannot verify hidden values from
  contradictory or unlabeled text alone.
- Require explicit disposition for every disagreement; don't silently edit
  the answer key to manufacture a perfect result.
- If fixture/source/rubric changes, produce a new digest, review version and
  re-check the affected cases. The old review must not be reused for new data.
- Record review scope, outcome, independent sign-off and evidence location.
  Only then may this gate be considered passed; **CI PASS is not sign-off**.

## Current blockers

- Reviewer not yet assigned; no blind assessment, adjudication or signed
  evidence exists.
- Research only: synthetic examples do not validate real invoices, OCR,
  cross-border VAT rules, recovery eligibility or economic outcomes.
- No public deployment, real uploads, live customer data or changes to other
  repositories. PR #21 stays **Draft**, merge **LOCKED**.
