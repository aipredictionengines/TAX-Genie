# BUILD-015 — signed audit checkpoint handoff (pilot)

## Implemented
Independent HMAC secret signs checkpoint metadata containing tenant, sequence, audit digest and issuance time. Verification detects checkpoint modification or disappearance/change of the specific anchored row.

## Not implemented
There is **no external storage transport**, WORM retention, timestamp authority, deployment KMS, key rotation, checkpoint scheduler or independent custody. In-memory/local anchors offer NO reliable rollback resistance if the attacker replaces both database and local checkpoint. Verification does not check all events by itself: combine with AuditJournal.verify and an independently retained latest checkpoint.

## Required external audit design
- A distinct trust boundary stores append-only checkpoints with authenticated UTC timestamps and independently managed keys.
- Encrypt/obfuscate tenant identity before exporting to a third-party store.
- Define anchoring cadence, alert on missed anchors, and make rollback/truncation alertable.
- Build issuer identity, key identifiers, KMS signing, revocation/rotation and operational runbooks.
- Obtain external penetration testing; verify malicious PDF isolation, malware scanner, network ingress controls, key lifecycle and right-to-erasure semantics.
- GDPR/privacy and DE→FR VAT rules stay under separate professional reviews.

Real customer invoices, production launch and Real PAPER 50 remain BLOCKED.
