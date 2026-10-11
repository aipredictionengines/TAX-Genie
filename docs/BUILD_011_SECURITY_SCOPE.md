# BUILD-011 — Structured extraction and subprocess isolation

## Added
- Explicitly labelled English/French-compatible alias extraction with conservative conflict checking and line provenance.
- A spawned-process PDF parsing prototype with 5 MiB input cap, max 20 pages, 250k extracted-text limit and worker termination on timeout.
- Unit tests on synthetic inputs only.

## Important limitations
- Parser subprocess is NOT integrated into the public/real-data API; a separately reviewed integration and deploy-specific safeguards are required.
- Multiprocessing spawn is not a hard sandbox. Production requires kernel/container isolation, unprivileged worker, network denial, filesystem restrictions, CPU/memory caps, malware scanning and safe resource limits.
- Basic bearer tokens remain pilot-only, without production IAM, revocation, rate limit or audit.
- No AI inference or real OCR here; extracted fields are unverified evidence candidates.
- No approved DE→FR VAT eligibility rules, no GDPR approval, no external security sign-off.
- Real invoices and public production remain prohibited.
