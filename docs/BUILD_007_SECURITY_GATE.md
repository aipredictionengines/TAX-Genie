# BUILD-007 — Security & privacy release gate (OPEN)

Repository: proofandsignal/TAX-Genie only. This file is a gate checklist, NOT a security certification.

## Evidence of bounded technical behavior
- Existing pilot API uses bearer-token tenant identification, tenant-scoped SQL access and AES-GCM encrypted document storage.
- Basic PDF checks limit size and page count; existing tests cover authorization, cross-tenant rejection and deletion.
- No external OCR or LLM transfer by default; no tax-refund authorization.

## Blockers before processing actual client invoices
- External security review and threat-model validation; test cross-tenant access and auth bypass comprehensively.
- Isolated malware scanning / sandboxed parser with time, memory and CPU limits.
- Production authorization, session/MFA, key rotation, revocation, audited secret management, TLS, rate limiting.
- Data-at-rest review: SQLite WAL, plaintext field metadata, backups, disk encryption and tenant isolation.
- Consent, purpose limitation, retention/deletion including backups, subject-rights flow, DPIA where required, DPA, data residency.
- Restrict extracted candidate fields and raw lines from API exposure; decide least-privilege access per role.
- Qualified EU VAT legal review remains in separate Draft PR #2.
- Real PAPER 50 requires consent, independent labels, and secure storage outside public GitHub.

## Release decision
SECURITY_GATE=BLOCKED
REAL_PAPER_50=BLOCKED
PRODUCTION=BLOCKED

Synthetic cohorts are parser regression checks only. Neither cohort establishes accuracy on real invoices.
