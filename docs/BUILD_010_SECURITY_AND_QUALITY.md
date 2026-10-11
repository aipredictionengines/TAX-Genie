# BUILD-010 — Security hardening + extraction (not production approval)

## Changes
- Parser accepts the explicit French label "Montant de TVA" without interpreting ambiguous tax charges as VAT.
- Existing frozen v2 cohort changes from 66.67% VAT recall to 100% only because that cohort informed development. **This is not independent validation.**
- New holdout v3 has 50 synthetic cases: 20 TP, 0 FP, 10 FN, 20 TN; precision 100%, recall 66.67%: **quality gate fails**.
- Pilot app rejects trivially weak (repeated-symbol) and malformed bearer tokens. This is an elementary configuration check, NOT proof of entropy or a production identity solution.

## Known security blockers
- No production token lifecycle, expiration, revocation, identity provider, MFA, audit trail or persistent brute-force controls.
- PDF processing happens in-process; no sandbox, malware scan, CPU/memory/time limit, or production-safe parser risk isolation.
- Local SQLite is unsuitable for promised regulated-grade tenant isolation; encryption key management, backups/WAL and deletion semantics require review.
- No tested production HTTPS setup, incident response exercise, DPIA, processor agreements or retention evidence.
- Tax eligibility rules still require qualified DE→FR review (independent draft PR #2).

## Gates
CI unit tests: pending.
Independent extraction quality: FAIL (synthetic v3 recall below 90%).
External security review: NOT DONE.
GDPR/privacy legal verification: NOT DONE.
Legal tax sign-off: NOT DONE.
Real PAPER 50: BLOCKED.
Public launch: BLOCKED.

Never upload client documents or claim that the system can determine refundable VAT.
