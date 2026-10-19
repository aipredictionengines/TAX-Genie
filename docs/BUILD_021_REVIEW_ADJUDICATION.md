# BUILD-021 — External annotation intake / disagreement triage (NOT a completed review)

The implementation is ready to accept a **future** human review of the 14-case
synthetic-only blind packet. No external reviewer has yet been assigned or
contacted and no independent decision or signature has been received.

## External first-pass procedure

1. Generate `python -m tax_genie.fixture_review_packet` and distribute **only its
   blind packet**, not GitHub links to the public author answer key.
2. The reviewer records their answers independently, before accessing any author
   labels or extraction output. For each of the **seven** named fields in **all
   14 cases**, annotate either `VALUE` with a source line and value or `ABSTAIN`
   with a nonempty reason. Record any required review flags.
3. The reviewer supplies the packet SHA-256, schema version
   `BUILD-021-REVIEW-V1`, role, review date and an **honest self-declaration**
   of independence. The self-declaration is **not verified evidence**.
4. Store original reviewer annotations, audit trail and reviewer identity in an
   access-controlled channel outside the **public** repository. Do not commit
   private identity, contact information, signatures, real invoices, or customer
   data here.
5. Separately compare the annotation JSON via
   `compare_review_submission(review_json)` after first-pass lock-in.
   Differences with author labels are flagged by case/field/issue category.
   No raw input text, field values or identity is included in the summary.
6. Every disagreement requires human adjudication; a zero-disagreement
   software result is **NOT** external sign-off. Independently verify the
   reviewer and the evidence record through an approved process.

### Submission shape (illustrative fragment only, NOT an actual review)

```json
{
  "schema": "BUILD-021-REVIEW-V1",
  "packet_sha256": "<the exact digest from the blind packet>",
  "reviewer_role": "vat_invoice_reviewer",
  "review_date": "YYYY-MM-DD",
  "independence_declared": false,
  "cases": [
    {
      "case_id": "QVAL-001",
      "fields": {
        "invoice_number": {"status": "ABSTAIN", "reason": "review pending"},
        "invoice_date": {"status": "ABSTAIN", "reason": "review pending"},
        "vat_id": {"status": "ABSTAIN", "reason": "review pending"},
        "country": {"status": "ABSTAIN", "reason": "review pending"},
        "currency": {"status": "ABSTAIN", "reason": "review pending"},
        "vat_amount": {"status": "ABSTAIN", "reason": "review pending"},
        "total_amount": {"status": "ABSTAIN", "reason": "review pending"}
      },
      "review_flags": []
    }
  ]
}
```

This example is **not valid as a completed submission**: all 14 distinct cases
are required and the sample judgments are placeholders.

The software's integration tests generate simulated review answers by copying
author expectations. This is **only a test fixture**, is not a blind review,
and MUST NEVER be submitted as outside evidence.

## Explicitly unsatisfied gates

- Independent human reviewer and reviewer independence verification: PENDING
- Independent annotations and adjudication: PENDING
- Original evidence/signature verification: PENDING
- Qualified DE→FR tax/legal signoff: PENDING
- Safe document ingestion, real malware scanner and sandbox: PENDING
- Real-client consent and privacy/security reviews: PENDING
- PR #21 merge: LOCKED
- Cloudflare deployment: LOCKED
