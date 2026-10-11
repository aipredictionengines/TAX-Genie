"""Frozen synthetic adversarial holdout v3.

Cohort is not used for tuning this build. No customer data.
"""
from .paper50 import evaluate

def make_holdout_v3():
    rows=[]
    for i in range(50):
        value=f"{i+15}.20"
        kind=i%5
        if kind==0:
            text=f"VAT Amount: {value}"
            truth={"vat_amount":value}
        elif kind==1:
            text=f"Montant de TVA: {value}"
            truth={"vat_amount":value}
        elif kind==2:
            text=f"VAT due: {value}"
            truth={"vat_amount":value}
        elif kind==3:
            text=f"Sales Tax: {value}"
            truth={}
        else:
            text=f"VAT Amount: {value}\nVAT Amount: 999.99"
            truth={}
        rows.append({"id":f"V3-{i:03d}","dataset":"synthetic","text":text,"truth":truth})
    return rows

def run():
    return evaluate(make_holdout_v3(), require_50=True)
