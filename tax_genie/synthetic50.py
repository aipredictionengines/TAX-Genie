"""Deterministic, entirely synthetic, zero-PII invoice benchmark cohort.

The expected values come from the fixture specification, never from extractor output.
"""
from __future__ import annotations
from .paper50 import evaluate

def make_cohort() -> list[dict]:
    rows=[]
    for index in range(50):
        number=f"SYN-{index+1:04d}"
        amount=f"{index+10}.25"
        total=f"{(index+10)*6}.50"
        truth={"invoice_number":number, "invoice_date":"2026-04-16",
               "vat_id":"FR12345678901", "country":"FR", "currency":"EUR",
               "vat_amount":amount, "total_amount":total}
        lines=[
            f"Invoice Number: {number}", "Invoice Date: 2026-04-16",
            "Supplier VAT ID: FR12345678901", "Supplier Country: FR",
            "Currency: EUR", f"VAT Amount: {amount}", f"Invoice Total: {total}",
        ]
        # Five deterministic families: clean, missing VAT, duplicate consistent,
        # conflicting VAT, and unlabeled VAT. Ground truth remains independent.
        family=index%5
        if family==1:
            lines=[line for line in lines if not line.startswith("VAT Amount:")]
            truth.pop("vat_amount")
        if family==2:
            lines.append(f"VAT Amount: {amount}")
        if family==3:
            lines.append("VAT Amount: 999.99")
            # Conflicting candidate values intentionally expected to be withheld.
            truth.pop("vat_amount")
        if family==4:
            lines=[("Tax "+line if line.startswith("VAT Amount:") else line) for line in lines]
            # The amount still exists semantically but is not supported by parser.
            # This is a deliberate extraction miss in benchmark ground truth.
        rows.append({"id":number,"dataset":"synthetic","text":"\n".join(lines),"truth":truth})
    return rows

def run() -> dict:
    return evaluate(make_cohort(), require_50=True)
