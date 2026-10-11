# BUILD-013 — security foundation, not production-ready

## Added
- Pilot in-memory per-tenant rate limiting wired into API authentication and tests. This is **not** distributed rate limiting or identity-grade throttling.
- Malware scanning is enforced at the API upload boundary and defaults to reject/unavailable (HTTP 503). No real scanner integrated; client uploads remain disabled. Synthetic tests inject a fake scanner explicitly.
- HMAC event digest utility, useful for future integrity checks. It is **not** a durable audit log.
- Existing AES-GCM encrypted PDF storage, tenant-scoped pilot records and bounded subprocess parsing remain.

## Security review blockers
- Wire a real supported malware scanner in a contained no-network document worker; prevent bypass and scan before parsing or persistence.
- Cloud edge/request body caps before JSON/base64 decoding; production IAM (revocation/MFA), HTTPS, centralized rate limiting, secret rotation.
- Independent OS sandbox with CPU/memory/FS/network restrictions and tested hostile PDFs.
- Durable tamper-evident audit journal, KMS-managed envelope encryption and secure backup/erasure.
- Penetration test and documented remediation, vendor DPA, privacy impact assessment and compliance signoff.

## Status
TECHNICAL_UNIT_TESTS: pending CI
PRODUCTION_SECURITY: BLOCKED
GDPR_PRIVACY: BLOCKED
DE_FR_VAT_LEGAL: BLOCKED (separate PR #2)
REAL_PAPER50: BLOCKED
CUSTOMER_LAUNCH: BLOCKED
