"""Build a blind, synthetic-only review packet for an EXTERNAL reviewer.

No ground-truth, supported_expected, extraction output, or answer key is in
the exported packet. This exporter does not perform an independent review.
"""
from __future__ import annotations

import hashlib
import json

from .quality_cohort_v1 import make_quality_cohort

PACKET_VERSION = "BUILD-021-BLIND-V1"
REVIEW_FIELDS = (
    "invoice_number", "invoice_date", "vat_id", "country",
    "currency", "vat_amount", "total_amount",
)


def build_blind_review_packet() -> dict:
    rows = make_quality_cohort()
    if len(rows) != 14 or len({row["id"] for row in rows}) != 14:
        raise ValueError("Unexpected fixture cohort; freeze must be reviewed")
    cases = [
        {"case_id": row["id"], "source_text": row["text"]}
        for row in rows
    ]
    core = {
        "version": PACKET_VERSION,
        "source": "authored_synthetic_text_only",
        "review_fields": list(REVIEW_FIELDS),
        "cases": cases,
    }
    canonical = json.dumps(
        core, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return {
        **core,
        "packet_sha256": hashlib.sha256(canonical).hexdigest(),
        "digest_scope": "canonical JSON of version, source, review_fields and cases",
        "review_status": "PENDING_EXTERNAL_REVIEW",
    }


def main() -> None:
    print(json.dumps(build_blind_review_packet(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
