# BUILD-018: Cloudflare foundation (proposal only)

## Scope
- Repository: `proofandsignal/TAX-Genie` only.
- Separate deployable entrypoint: `cloudflare/worker/`.
- No changes to the existing Python/FastAPI backend or BUILD-017 external custody adapter.
- The initial Worker deliberately does **not** accept invoice uploads, create cases, read documents, or connect to any database. Everything except `GET /health` returns HTTP 503.
- Health reports `production_ready:false`. This is a synthetic bootstrap and is not a working Tax Genie API.
- R2, D1, Queues, secrets, GitHub deploy integration, custom domains, and customer data are **not** configured in this phase.

## Why the earlier deployment failed
Cloudflare attempted `npx wrangler deploy` in the root of the Python repository, which contains no Cloudflare Worker entrypoint. A successful `pip install` did not make FastAPI deployable as a Worker. Use the isolated subdirectory configuration instead.

## Local tests (Node 20+)
```sh
cd cloudflare/worker
npm install
npm test
npm run build
```
The build command uses `wrangler deploy --dry-run`; it does not publish resources.

## Future GitHub-connected Workers Builds configuration (not yet approved)
- Repository: `proofandsignal/TAX-Genie` only
- Root directory: `cloudflare/worker`
- Production branch: `main` only AFTER review, CI and explicit go-ahead
- Build command: `npm run build`
- Deploy command: `npm run deploy`
- Do not reconnect automatic production deploy until BUILD-018 has passed review and environment isolation checks.
- The previous `tax-genie-api` Worker was reported deleted. The replacement is named `tax-genie-worker`; do not recreate it automatically.
- `workers_dev:false` requires an explicit future route/custom-domain deployment strategy. Never enable public test endpoints by default.

## Future resource verification gate
The user reported no D1 or R2 resources created. Confirm absence directly before creating `tax-genie-db` and `tax-genie-documents`. Set Block Public Access / no public bucket access and separate project-scoped permissions. Do not insert actual invoices or customer records. D1 and R2 bindings need their real resource identifiers and should only be added in an isolated reviewed follow-on PR.

## Production blockers
Qualified DE→FR tax-law reviewer and GDPR/security review; threat model; tenant isolation; real malware scanning; hardened PDF processing; benchmark showing adequate recall; encryption/key rotation; retention policy; independent immutable audit custody and restore tests. None is waived by a green Cloudflare dry run.
