"""Compare a submitted external first-pass annotation with authored synthetic labels.

This module validates structure and identifies disagreements, NOT reviewer
independence, legal correctness, signature authenticity or approval for merge.
The output contains case IDs, fields and issue categories only: no raw text,
invoice amounts or reviewer identity.
"""
from __future__ import annotations

from datetime import date

from .fixture_review_packet import build_blind_review_packet, REVIEW_FIELDS
from .quality_cohort_v1 import make_quality_cohort

REVIEW_SCHEMA = "BUILD-021-REVIEW-V1"
ALLOWED_ROLES = {"vat_invoice_reviewer", "document_quality_reviewer"}
REVIEW_FIELD_SET = frozenset(REVIEW_FIELDS)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _validate_submission(submission: dict, packet: dict) -> dict:
    _require(isinstance(submission, dict), "Review submission must be a dict")
    _require(set(submission) == {
        "schema", "packet_sha256", "reviewer_role", "review_date",
        "independence_declared", "cases",
    }, "Invalid review submission fields")
    _require(submission["schema"] == REVIEW_SCHEMA, "Invalid review schema")
    _require(submission["packet_sha256"] == packet["packet_sha256"], "Review packet digest mismatch")
    _require(submission["reviewer_role"] in ALLOWED_ROLES, "Invalid reviewer role")
    _require(type(submission["independence_declared"]) is bool, "Invalid independence declaration")
    _require(isinstance(submission["review_date"], str), "Invalid review date")
    try:
        date.fromisoformat(submission["review_date"])
    except ValueError as exc:
        raise ValueError("Invalid review date") from exc

    submitted = submission["cases"]
    _require(isinstance(submitted, list), "Review cases must be a list")
    expected_ids = {row["case_id"] for row in packet["cases"]}
    ids = []
    by_id = {}
    for record in submitted:
        _require(isinstance(record, dict) and set(record) == {
            "case_id", "fields", "review_flags"
        }, "Invalid case review structure")
        cid = record["case_id"]
        _require(isinstance(cid, str), "Invalid review case ID")
        ids.append(cid)
        _require(isinstance(record["fields"], dict) and set(record["fields"]) == REVIEW_FIELD_SET,
                 "Seven reviewed field decisions are required")
        for field, annotation in record["fields"].items():
            _require(isinstance(annotation, dict) and annotation.get("status") in {"VALUE", "ABSTAIN"},
                     "Invalid review field status")
            if annotation["status"] == "VALUE":
                _require(set(annotation) == {"status", "value", "line"}
                         and isinstance(annotation["value"], str) and bool(annotation["value"])
                         and type(annotation["line"]) is int and annotation["line"] > 0,
                         "Malformed source-backed value")
            else:
                _require(set(annotation) == {"status", "reason"}
                         and isinstance(annotation["reason"], str) and bool(annotation["reason"].strip())
                         and len(annotation["reason"]) <= 240, "Malformed abstention reason")
        flags = record["review_flags"]
        _require(isinstance(flags, list) and all(
            isinstance(flag, str) and flag and len(flag) <= 80 for flag in flags
        ) and len(set(flags)) == len(flags), "Invalid review flag list")
        by_id[cid] = record
    _require(len(ids) == len(expected_ids) and set(ids) == expected_ids
             and len(set(ids)) == len(ids), "Missing, extra or duplicate review cases")
    return by_id


def compare_review_submission(submission: dict) -> dict:
    """Accept a candidate review and report discrepancies; NEVER mark verified."""
    packet = build_blind_review_packet()
    reviewed = _validate_submission(submission, packet)
    authored = {row["id"]: row for row in make_quality_cohort()}
    source = {row["case_id"]: row["source_text"].splitlines() for row in packet["cases"]}
    issues = []
    for cid in sorted(reviewed):
        record = reviewed[cid]
        baseline = authored[cid]
        lines = source[cid]
        for field in REVIEW_FIELDS:
            judgment = record["fields"][field]
            expected = baseline["supported_expected"].get(field)
            if judgment["status"] == "VALUE":
                if judgment["line"] > len(lines):
                    issues.append({"case_id": cid, "field": field, "issue": "line_out_of_range"})
                if expected is None:
                    issues.append({"case_id": cid, "field": field, "issue": "review_asserted_unsupported"})
                elif judgment["value"] != expected:
                    issues.append({"case_id": cid, "field": field, "issue": "value_disagreement"})
            elif expected is not None:
                issues.append({"case_id": cid, "field": field, "issue": "review_abstained_supported"})
        for flag in baseline["required_review_flags"]:
            if flag not in record["review_flags"]:
                issues.append({"case_id": cid, "field": "review_flags", "issue": "missing_author_flag"})
        for flag in record["review_flags"]:
            if flag not in baseline["required_review_flags"]:
                issues.append({"case_id": cid, "field": "review_flags", "issue": "reviewer_added_flag"})
    return {
        "schema": REVIEW_SCHEMA,
        "packet_sha256": packet["packet_sha256"],
        "synthetic_case_count": len(reviewed),
        "disagreement_count": len(issues),
        "disagreements": issues,
        "independence_declared": submission["independence_declared"],
        "independence_verified": False,
        "external_signoff_verified": False,
        "review_gate": "PENDING_HUMAN_ADJUDICATION_AND_SIGNOFF",
        "note": "Comparison is not evidence of an independent review or permission to merge.",
    }
