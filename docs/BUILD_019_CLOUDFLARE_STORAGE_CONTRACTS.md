# BUILD-019: Isolated D1/R2 storage contracts — synthetic-only

## Scope
- Proposed resources: D1 `tax-genie-db`, private R2 `tax-genie-documents`.
- Namespaced bindings: `TAX_GENIE_DB`, `TAX_GENIE_DOCUMENTS`.
- Storage helper is **not connected** to the Worker entrypoint. It does not execute D1 queries or R2 reads/writes.
- D1 schema is **proposal only**, and no migration has been run. R2 bucket has not been created.
- Keys are derived from explicit tenant/case/object IDs with strict character validation; key prefixing is defense in depth **not authentication/authorization**.
- Never accept a tenant identifier from an untrusted caller without comparing it against authenticated server-side tenant context.
- No live PDF, invoice, credential, customer, or other sensitive data.
- Do not add D1 or R2 binding placeholders that pretend a real resource ID exists.
- No public R2 domain, workers.dev preview, or automatic deployment.
- Cloudflare account shared across projects, resources distinct. Do not read or mutate other projects.

## D1 invariants
- `PRAGMA foreign_keys=ON` for connections executing mutations.
- Queries must bind tenant_id from authenticated context and use prepared statements.
- D1 is not an immutable external audit source.
- Schema intentionally holds only opaque identifiers and lifecycle state; real PII must await privacy/security approval.

## Next gate
Verify account inventory and capability, create explicitly named isolated resources only on approval; then reviewed Wrangler binding configuration with actual D1 ID and private R2 bucket; mocked cross-tenant and fail-closed tests; security review before any active API paths.

## Non-goals
- Neither this branch nor BUILD-018 implements document upload, PDF parsing, VAT extraction, production authentication, billing, independent audit custody, or human tax review.
