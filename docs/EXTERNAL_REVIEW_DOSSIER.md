# Tax Genie — External reviewer dossier (OPEN, not approved)

## Scope
International B2B-first recovery intelligence; first jurisdiction route DE-establishment → FR VAT. No tax filing, no production customer invoice processing, no guaranteed refunds.

## Security reviewer package
- Inspect intake: tax_genie/intake.py; API: tax_genie/api.py; OCR adapter: tax_genie/document_adapter.py.
- Review tenant token model, authentication bypasses, rate limiting, PDF sandbox, malware handling, AES-GCM key lifecycle, secret rotation, secure transport, tenant segregation, backups, audit and incident response.
- Test upload abuse: malformed/hostile PDFs, exhaustion, malformed API bodies, cross-tenant document access and delete consistency.
- Required signed output: threat model, critical/high findings, remediation evidence, signed report, reviewer credentials/date.

## GDPR/privacy reviewer package
- Identify controllers/processors, legal bases and purposes for actual planned processing; determine DPIA requirements.
- Record data inventory, minimization, data residency and subprocessors; retention, erasure, backups, DPA and data-subject access and breach reporting.
- Prohibit use of production data until independent written review and all necessary controls exist.

## DE→FR VAT expert package
- Verify official EU and French/German sources and effective dates, claim thresholds, scope, exclusions, place-of-supply and claimant eligibility, prior claims and deadlines.
- Record rule-by-rule signoff, reviewer qualifications, date and caveats. PR #2 remains separate and unapproved.

## Quality package
- Freeze candidate parser and test cohort; report raw confusion matrices per field and separate synthetic vs consented-real.
- Use representative real-world layouts only after privacy/security release and human verified ground truth.
- Proposed field thresholds: precision ≥0.95, recall ≥0.90. No automatic tax eligibility approval.

## Current review status
- Security: NOT REVIEWED INDEPENDENTLY
- Privacy: NOT REVIEWED INDEPENDENTLY
- Tax law: NOT SIGNED OFF
- Real PAPER 50: NOT STARTED
- Production: BLOCKED

No legal or security accreditation is claimed by this document.
