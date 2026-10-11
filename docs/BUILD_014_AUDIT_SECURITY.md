# BUILD-014 — Durable audit journal (pilot, not production accreditation)

Scope: add tenant-scoped chained HMAC audit records for minimal event kinds, append within SQLite transactions, and detect modifications under a separate secret.

Properties: event allowlist, no raw case identifiers in audit records, per-tenant hash chain, and integrity verification.

Limits: **SQLite is mutable**; truncation of a tail, full-database rollback, database replacement, event omission, key compromise, clock tampering, and privileged actor attacks are NOT prevented. Do not claim WORM, immutable storage, full forensic auditability, or complete audit coverage.

External requirements: write-once off-host audit sink with externally anchored checkpoints, KMS-derived separately rotated keys, redacted access policy, operator accountability, isolated scanning service, parser OS sandbox, ingress body caps, distributed rate limiting, MFA/identity, penetration test, GDPR counsel review and DE→FR VAT expert signoff.

Customer uploads remain blocked by default without a real malware scanner. Public production and real PAPER 50 remain BLOCKED.
