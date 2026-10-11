"""Structured candidate parser for deterministic, labelled synthetic invoice text.

This adapter never claims tax eligibility and intentionally rejects ambiguity.
"""
import re
from .invoice_evidence import extract_invoice_evidence

LABELS = {
    "vat_amount": ("montant tva", "montant de tva", "vat payable", "vat due"),
    "total_amount": ("amount payable", "total payable", "total including vat"),
    "currency": ("invoice currency",),
    "invoice_date": ("date of issue",),
}
AMOUNT = re.compile(r"^[0-9]{1,10}(?:\.[0-9]{1,2})?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
def parse_structured_text(text: str) -> dict:
    if not isinstance(text, str) or len(text)>250_000:
        raise ValueError("Invalid input")
    normalized=[]
    # Parse only exact key:value or key=value labelled lines. No table inference.
    for line in text.splitlines():
        if len(line)>500:
            normalized.append(line)
            continue
        match=re.fullmatch(r"\s*([\w ]{2,45})\s*[:=]\s*(.*?)\s*",line,re.I)
        if match:
            label=" ".join(match.group(1).casefold().split())
            value=match.group(2)
            for field,aliases in LABELS.items():
                if label in aliases:
                    if field in ("vat_amount","total_amount") and AMOUNT.fullmatch(value):
                        canonical="VAT Amount" if field=="vat_amount" else "Invoice Total"
                        line=f"{canonical}: {value}"
                    elif field=="currency" and re.fullmatch(r"[A-Za-z]{3}",value):
                        line=f"Currency: {value}"
                    elif field=="invoice_date" and DATE.fullmatch(value):
                        line=f"Invoice Date: {value}"
                    break
        normalized.append(line)
    result=extract_invoice_evidence("\n".join(normalized))
    result["method"]="structured_alias_v0.1"
    result["review_status"]="HUMAN_REVIEW_REQUIRED"
    result["refund_eligibility"]="UNDETERMINED"
    return result
