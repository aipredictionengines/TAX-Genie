# BUILD-016 — External audit custody interface and key rotation model

## Shipped in code (pilot contract)
- Defined publish/retrieve protocol for independently retained signed checkpoints.
- Default external custody is DISABLED / fail-closed.
- Synthetic in-memory implementation only for unit tests (not independent or durable).
- Caller-supplied, versioned key IDs, rotation by explicit selection of preprovisioned key; old checkpoints remain verifiable while old keys remain available.
- Tests for absent custody, changed audit row, old/new key verification and weak key rejection.

## Still blocking production
- No actual remote external storage service, no external receipts, no WORM enforcement, no KMS integration, no managed secret vault, no independently verified timestamp, no automated scheduling or checkpoint retention monitoring.
- No cryptographic key destruction policy, rotation procedure or compromise-recovery playbook.
- Signature on one retained checkpoint is not complete chain verification. AuditJournal.verify must be combined with independently held latest checkpoint; tail rollback cannot be ruled out without a trusted latest external copy.
- Malware gate remains fail-closed without a real configured scanner. PDF worker is not an OS sandbox and the pilot auth/rate limiter are not production-grade.
- Qualified DE→FR VAT review (PR #2), security assessment, GDPR assessment and new untuned quality evaluation remain open.

No real customer invoices and no public launch.
