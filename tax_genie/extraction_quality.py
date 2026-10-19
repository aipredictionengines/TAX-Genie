"""BUILD-021: evidence-bounded extraction quality gate (synthetic-only).

This is not a VAT eligibility test or an estimate of real-world field accuracy.
The evaluator does not transmit, persist, or include raw invoice lines in reports.
"""
from __future__ import annotations
from collections import defaultdict
from .invoice_evidence import FIELDS, PATTERNS, extract_invoice_evidence


def evaluate_quality(rows: list[dict], *, extractor=extract_invoice_evidence) -> dict:
    if not isinstance(rows, list) or not rows:
        raise ValueError("Nonempty synthetic cohort required")
    identifiers = [row.get("id") for row in rows]
    if any(not isinstance(x, str) or not x for x in identifiers) or len(set(identifiers)) != len(rows):
        raise ValueError("Unique case IDs required")
    fields = set(FIELDS)
    totals = defaultdict(int)
    families = defaultdict(int)
    failures = []
    for row in rows:
        if row.get("dataset") != "synthetic":
            raise ValueError("Only synthetic rows may enter BUILD-021")
        if not isinstance(row.get("text"), str) or not isinstance(row.get("family"), str):
            raise ValueError("Invalid synthetic fixture")
        semantic = row.get("semantic_truth")
        supported = row.get("supported_expected")
        required_flags = row.get("required_review_flags")
        if (
            not isinstance(semantic, dict) or not isinstance(supported, dict)
            or set(semantic) - fields or set(supported) - fields
            or any(not isinstance(v, str) for v in list(semantic.values()) + list(supported.values()))
            or not isinstance(required_flags, list)
            or any(not isinstance(x, str) for x in required_flags)
        ):
            raise ValueError("Invalid independent truth or safe-extraction specification")
        if any(semantic.get(k) != v for k, v in supported.items()):
            raise ValueError("Safe extraction cannot contradict semantic truth")
        result = extractor(row["text"])
        if not isinstance(result, dict) or not isinstance(result.get("fields"), dict):
            failures.append({"id": row["id"], "issue": "invalid_extractor_result"})
            continue
        predicted = {}
        source_lines = row["text"].splitlines()
        for field, candidate in result["fields"].items():
            if field not in fields or not isinstance(candidate, dict) or not isinstance(candidate.get("value"), str):
                failures.append({"id": row["id"], "issue": "invalid_candidate"})
                continue
            line_number = candidate.get("line")
            valid_origin = (
                type(line_number) is int
                and 1 <= line_number <= len(source_lines)
                and candidate.get("method") == "labeled_regex"
            )
            if valid_origin:
                match = PATTERNS[field].fullmatch(source_lines[line_number - 1])
                origin_value = None if match is None else match.group(1)
                if origin_value is not None and field in {"currency", "vat_id", "country"}:
                    origin_value = origin_value.upper()
                valid_origin = origin_value == candidate["value"]
            if not valid_origin:
                failures.append({"id": row["id"], "issue": "invalid_provenance", "field": field})
            predicted[field] = candidate["value"]
        families[row["family"]] += 1
        totals["cases"] += 1
        for field in FIELDS:
            expected = supported.get(field)
            actual = predicted.get(field)
            truth = semantic.get(field)
            if expected is None:
                if actual is None:
                    totals["correct_abstentions"] += 1
                    if truth is None:
                        totals["correct_negative_abstentions"] += 1
                    else:
                        totals["safe_abstentions_on_known_truth"] += 1
                else:
                    totals["unsafe_assertions"] += 1
                    failures.append({"id": row["id"], "issue": "unsafe_assertion", "field": field})
            else:
                totals["supported_fields"] += 1
                if actual == expected:
                    totals["correct_supported_fields"] += 1
                else:
                    totals["missed_or_wrong_supported"] += 1
                    failures.append({"id": row["id"], "issue": "supported_field_mismatch", "field": field})
            if truth is not None:
                totals["semantic_known_fields"] += 1
                if actual == truth:
                    totals["semantic_exact_fields"] += 1
        flags = result.get("review_flags")
        if not isinstance(flags, list) or any(not isinstance(flag, str) for flag in flags) or not set(required_flags).issubset(set(flags)):
            totals["missing_required_flags"] += 1
            failures.append({"id": row["id"], "issue": "missing_required_review_flag"})
        if (
            result.get("refund_eligibility") != "UNDETERMINED"
            or result.get("recoverable_amount") is not None
            or result.get("review_status") != "HUMAN_REVIEW_REQUIRED"
        ):
            totals["policy_violations"] += 1
            failures.append({"id": row["id"], "issue": "unapproved_tax_conclusion"})
    supported_total = totals["supported_fields"]
    semantic_total = totals["semantic_known_fields"]
    return {
        "dataset": "synthetic",
        "total_cases": totals["cases"],
        "families": dict(sorted(families.items())),
        "metrics": dict(sorted(totals.items())),
        "supported_exact_rate": None if not supported_total else round(totals["correct_supported_fields"] / supported_total, 4),
        "semantic_exact_coverage": None if not semantic_total else round(totals["semantic_exact_fields"] / semantic_total, 4),
        "passed": not failures,
        "failures": failures,
        "limits": "Synthetic text fixture only; neither real invoice accuracy, eligibility nor recoverable VAT is established.",
    }
