"""New synthetic holdout, authored separately from parser changes.

Freeze this cohort before future parser improvements. No real customer data.
"""
from __future__ import annotations
from .paper50 import evaluate

def frozen_holdout_v2() -> list[dict]:
    rows=[]
    for i in range(50):
        amount=f"{i+11}.75"
        mode=i % 5
        if mode==0:
            text=f"VAT Amount: {amount}"
            truth={"vat_amount":amount}
        elif mode==1:
            text=f"TVA totale: {amount}"
            truth={"vat_amount":amount}
        elif mode==2:
            text=f"Montant de TVA: {amount}"
            truth={"vat_amount":amount}
        elif mode==3:
            text=f"VAT Amount: {amount}\nVAT Amount: 999.99"
            truth={}
        else:
            text=f"Sales Tax: {amount}"
            truth={}
        rows.append({"id":f"V2-{i+1:03d}", "dataset":"synthetic", "text":text, "truth":truth})
    return rows

def run_holdout_v2() -> dict:
    return evaluate(frozen_holdout_v2(),require_50=True)
