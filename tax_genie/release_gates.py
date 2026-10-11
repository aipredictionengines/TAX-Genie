"""Machine-readable evidence gate: defaults to BLOCKED; never self-certifies."""
from __future__ import annotations

GATES = (
    "independent_quality", "production_security", "privacy_gdpr",
    "eu_vat_legal", "real_paper50"
)

def release_readiness(evidence: dict[str,dict] | None = None) -> dict:
    evidence=evidence or {}
    gates={}
    for gate in GATES:
        record=evidence.get(gate,{})
        approved=(record.get("approved") is True
                  and bool(record.get("reviewer"))
                  and bool(record.get("evidence_reference"))
                  and bool(record.get("verified_at")))
        gates[gate]={"status":"REVIEW_SUBMITTED" if approved else "BLOCKED",
                     "requires_independent_verification":True}
    # Submitting metadata isn't independent verification.
    return {"public_launch":"BLOCKED","real_customer_documents":"BLOCKED",
            "gates":gates,
            "explanation":"No release is possible through self-reported metadata alone."}
