"""BUILD-021: deliberately small frozen SYNTHETIC extraction-quality fixture.

Semantic truth is authored separately from what is safely inferable from text.
Never use this cohort as evidence of live-document performance.
"""
from __future__ import annotations

# id, family, VAT text, semantic VAT truth, safe-to-extract VAT, required flag.
# Ground truth and expected safe outputs are specified BEFORE running the parser.
_CASES = (
    ("QVAL-001", "explicit", "VAT Amount: 20.00", "20.00", "20.00", None),
    ("QVAL-002", "explicit", "Montant de TVA: 15.50", "15.50", "15.50", None),
    ("QVAL-003", "duplicate_consistent", "VAT Amount: 10.00\nVAT Amount: 10.00", "10.00", "10.00", None),
    ("QVAL-004", "duplicate_consistent", "TVA totale: 18.25\nTVA totale: 18.25", "18.25", "18.25", None),
    ("QVAL-005", "missing", "", None, None, "MISSING_VAT_AMOUNT"),
    ("QVAL-006", "missing", "No additional tax shown", None, None, "MISSING_VAT_AMOUNT"),
    ("QVAL-007", "non_vat_tax", "Sales Tax: 11.00", None, None, "MISSING_VAT_AMOUNT"),
    ("QVAL-008", "non_vat_tax", "Tax Amount: 13.00", None, None, "MISSING_VAT_AMOUNT"),
    ("QVAL-009", "conflicting", "VAT Amount: 20.00\nVAT Amount: 22.00", "20.00", None, "CONFLICTING_VAT_AMOUNT"),
    ("QVAL-010", "conflicting", "VAT Amount: 30.00\nVAT Amount: 29.00", "30.00", None, "CONFLICTING_VAT_AMOUNT"),
    ("QVAL-011", "unlabelled", "Tax line 12.00 EUR", "12.00", None, "MISSING_VAT_AMOUNT"),
    ("QVAL-012", "unlabelled", "VAT? 14.00 EUR", "14.00", None, "MISSING_VAT_AMOUNT"),
    ("QVAL-013", "arithmetic_conflict", "VAT Amount: 150.00", "150.00", "150.00", "VAT_EXCEEDS_TOTAL"),
    ("QVAL-014", "arithmetic_conflict", "VAT Amount: 125.00", "125.00", "125.00", "VAT_EXCEEDS_TOTAL"),
)


def make_quality_cohort() -> list[dict]:
    rows = []
    for case_id, family, vat_lines, semantic_vat, supported_vat, flag in _CASES:
        base = {
            "invoice_number": case_id,
            "invoice_date": "2026-04-16",
            "vat_id": "FR12345678901",
            "country": "FR",
            "currency": "EUR",
            "total_amount": "120.00",
        }
        semantic_truth = dict(base)
        supported_expected = dict(base)
        if semantic_vat is not None:
            semantic_truth["vat_amount"] = semantic_vat
        if supported_vat is not None:
            supported_expected["vat_amount"] = supported_vat
        text = "\n".join([
            "Invoice Number: " + case_id,
            "Invoice Date: 2026-04-16",
            "Supplier VAT ID: FR12345678901",
            "Supplier Country: FR",
            "Currency: EUR",
            "Invoice Total: 120.00",
            vat_lines,
        ])
        rows.append({
            "id": case_id,
            "dataset": "synthetic",
            "family": family,
            "text": text,
            "semantic_truth": semantic_truth,
            "supported_expected": supported_expected,
            "required_review_flags": [flag] if flag else [],
        })
    return rows
