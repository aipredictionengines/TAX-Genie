# Tax Genie — Verification Agent v0.1 (DESIGN ONLY, NO LIVE EXECUTION)

Date: 2026-10-19. Scope: Germany–France as first research corridor, international only.
Status: **DESIGN PROPOSED / UNIMPLEMENTED**. This file is not a deployed monitoring service, legal rules engine, tax advisor or tax-filing capability.

## Reason for building

A VAT registration check is not proof of refund eligibility. A syntactically valid invoice is not evidence of correct tax treatment, and a potentially eligible line is not money recovered.

The goal is to lower the long-run cost of independent, reviewable evidence gathering without replacing independent domain sign-off. A Proof & Signal agent **cannot be an independent auditor of its own fixture labels**. BUILD-021 external fixture review stays blocked.

## Evidence pipeline — no legal auto-decisions

1. **SOURCE DISCOVERY** — Allowlist official EU, German and French authorities, legal texts, standard bodies, and release notes; mark every entry with jurisdiction, subject, canonical link, publication/updated date and legal/effective date where directly stated.
2. **CHANGE CAPTURE** — Compare version/release identifiers and content hashes of publicly available pages/documents. Save timestamp, provenance, before/after excerpts, source version and verification status. Page changes alone are NOT proof of a changed rule. Avoid prohibited automated access, paywalled standards, or CAPTCHA bypass.
3. **CROSS-CHECK** — Classify `EDITORIAL_CHANGE`, `STANDARD_ARTIFACT_UPDATE`, `OFFICIAL_RULE_CHANGE_CANDIDATE`, `DEADLINE_CHANGE_CANDIDATE`, `SOURCE_UNAVAILABLE`. For legal changes, cross-reference the actual legal text and relevant national tax authority before interpretation.
4. **RULE PROPOSAL** — Store an auditable proposal: exact jurisdiction, taxable-person profile, type of invoice/expense, relevant legal provision, version, effective date and unknowns. Never enable proposed rules automatically. Annotate `LEGAL_SIGNOFF_PENDING`.
5. **INVOICE EVIDENCE** — Synthetic invoice fields receive `SOURCE_BACKED_CANDIDATE` or `ABSTAIN_HUMAN_REVIEW`; keep source line or machine-readable field path and provenance. VAT number format/VIES checks, EN16931 syntax checks, and invoice arithmetic are different controls. None alone determines recoverability.
6. **REVIEW GATE** — Independent tax professional validates materially consequential tax conclusions. Manual review of only uncertain/high-cost cases can be explored **after** the methodology and risk threshold are externally approved.
7. **OUTCOME ECONOMICS** — Separately measure test-set candidate precision/coverage, reviewer corrections, required manual-review share, compute/source/monitoring cost, legal-review cost and delivered customer value. VAT recovered is reported only with actual payment/authority-backed proof (none exists).

### Initial sources (not a full or verified legal rule register)

| Key | Official source | Why track | No-go assumption |
|---|---|---|---|
| EU_REFUND | https://taxation-customs.ec.europa.eu/taxation/vat/vat-directive/vat-refunds_en | Cross-border refund framework and links to official procedures | Refund rights cannot be inferred from a VAT number |
| EU_2008_9 | https://eur-lex.europa.eu/eli/dir/2008/9/oj | EU-established taxpayer cross-border refund directive and consolidated amendments | Current applicability and national restrictions require legal verification |
| EU_VAT | https://eur-lex.europa.eu/eli/dir/2006/112/oj | EU VAT Directive legal changes | Directive text alone does not resolve transaction-specific applicability |
| EU_VIDA | https://taxation-customs.ec.europa.eu/taxation/vat/vat-digital-age-vida_en | ViDA implementation schedule and changes | Draft updates / programme posts are not enacted rules |
| EN16931 | https://ec.europa.eu/digital-building-blocks/sites/spaces/DIGITAL/pages/467108661/European+Standard+and+Specifications | EN 16931-1 version and transition information | Public page does not grant access to paywalled full standard |
| EN16931_ARTEFACTS | https://ec.europa.eu/digital-building-blocks/sites/spaces/EINVCOMMUNITY/pages/113541173/Updates+to+the+Registry+of+supporting+artefacts | Official validation releases and code lists | Validator release is not independently a tax-law change |
| FR_EINVOICE | https://ec.europa.eu/digital-building-blocks/sites/spaces/einvoicingCFS/pages/956171282/2026+France+2026+eInvoicing+Country+Sheet | French implementation overview; verify against DGFiP | Country sheet may be stale or not authoritative for legal interpretation |
| DE_EINVOICE | https://ec.europa.eu/digital-building-blocks/sites/spaces/einvoicingCFS/pages/956171283/2026+Germany+2026+eInvoicing+Country+Sheet | German implementation overview; verify against BMF/BZSt | Country sheet may be stale or not authoritative for legal interpretation |
| DE_BZST | https://online.portal.bzst.de/SharedDocs/Leistungsbeschreibung/DE/vorsteuerverguetung_auslaendische_unternehmer_in_eu.html | German refund application workflow | Portal text does not establish a particular claimant's eligibility |

Critical observed research leads to verify before any engineering implementation:
- EN 16931-1: 2026 edition published May 2026; transition from 2017 edition.
- EN 16931 validation artefacts: official release 1.3.17 on October 12, 2026.
- FR and DE phased e-invoicing mandates and dates differ; track country-specific effective dates.
- ViDA package, enacted 2025, phased to 2035. Do NOT equate future legal implementation dates with current obligations.

## Expected proposed data contract (not implemented)

```json
{
  "signal_id": "proposed",
  "source_key": "EN16931_ARTEFACTS",
  "source_url": "official_url",
  "retrieved_at": "UTC timestamp",
  "published_at": null,
  "effective_from": null,
  "current_version": null,
  "evidence_digest": null,
  "change_type": "STANDARD_ARTIFACT_UPDATE",
  "status": "SOURCE_CHANGED_UNVERIFIED",
  "country": ["DE", "FR"],
  "impact_hypothesis": "manual evaluation needed",
  "legal_signoff": "PENDING",
  "auto_apply": false
}
```

## Version 0.1 acceptance / security gates

- Synthetic change fixtures only; deterministically report changed/not changed/unavailable, with source URL/version and no invented legal consequence.
- Fail closed on source outage, renamed URL, parsing ambiguity, out-of-order effective dates, inaccessible licence, or conflicting authorities.
- Signed/immutable custody of relevant source snapshots requires later dedicated design and review; no claim it exists.
- Recheck declared effective date separately from date of publication; never overwrite previously applicable law without human sign-off.
- No unapproved crawlers, website accounts, API scraping, unattended code updates, Cloudflare resources or public deployment.
- BUILD-021 remains **DRAFT**, its 14 fixture source texts and author labels are frozen pending a real independent external review.
- No external document intake, client PII, eligibility claims, expected VAT refunds or authority submissions.

## Commercial validation — parallel, separate gate

Prospects must be **DISCOVERED → DEDUPED → WORKFLOW CHECKED → CONTACT VERIFIED → OUTREACH APPROVED → RESPONSE MEASURED**. An official partnership program signals that a company accepts partner applications, not that it wants this product. No sales/paid pilot/partnership may be claimed before a real reply and explicit agreement. A first 15-minute discovery call should ask: monthly invoice volume, common VAT-data errors, review time, cost per exception, required country/format coverage, and whether a no-PII synthetic demonstration is worth evaluating. No real document sample is requested before privacy/security and legal approvals.

No merges or deployments authorized by this file.
