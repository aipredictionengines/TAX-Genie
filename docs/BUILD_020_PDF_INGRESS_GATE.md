# BUILD-020 — Secure PDF ingress preflight, phase 1

The existing pilot already runs a bounded PDF subprocess and uses a fail-closed scanner interface. Neither constitutes a hardened OS sandbox or a production-grade malware scanning integration.

This phase adds a deterministic, testable **preflight policy** for synthetic PDFs:
- explicit PDF filename extension and no path separators or NUL;
- bounded content size using existing MAX_BYTES;
- PDF version header check;
- rejection of invalid metadata before scanner invocation;
- a composed helper that only returns true when an explicitly configured scanner returns literal `True`.

## Security limitations

A correct PDF header is not proof a file is valid, benign, or parseable. These helpers are not wired into production upload routes. No new client-facing functionality is unlocked. Scanner implementations, cloud queue, hardened isolation, decompression and parser resource budgets require separate implementation and review.

**No real customer invoices, live uploads, Cloudflare deployment, D1/R2 provisioning or merge approved by this phase.**
