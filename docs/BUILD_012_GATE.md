# BUILD-012 — Bounded subprocess integrated, public launch BLOCKED

## Built
- PDF upload processing now calls bounded spawned-process parsing, not direct in-process PdfReader.
- Parser rejects invalid, encrypted, overly large or timed-out PDFs; exceptions are not echoed as sensitive details to API consumers.
- Existing encrypted persistence and per-tenant query filters remain.
- Synthetic v4 50-case candidate extraction holdout, intentionally not tuned to parser.

## Limits
- This subprocess is **not** a security sandbox: no malware scanner, seccomp, OS-level resource cap, network isolation, unprivileged execution, key rotation, signed independent audit, or GDPR sign-off.
- The current HTTP JSON/base64 upload path still lacks request-body ingress limits, rate limiting, real identity and operational audit.
- No real PDF corpus, no OCR, and no expert-approved DE-FR tax rules. Real PAPER 50 and any public deployment remain blocked.
- Synthetic holdout v4 expected VAT precision=100%, recall=66.67%, so quality criterion ≥90% recall still fails.

## Required next gates
Independent prospective representative holdout; OS isolation and request limits; external security/privacy review; qualified DE-FR VAT legal signoff; consented real invoices held exclusively in secured infrastructure.
