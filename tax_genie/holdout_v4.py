"""Frozen prospective synthetic parser holdout. Not real-invoice or OCR evidence."""
from .paper50 import evaluate

def cohort():
    rows = []
    for i in range(50):
        amount=f"{i+30}.40"
        kind=i%5
        if kind==0:
            text=f"VAT Amount: {amount}"; truth={"vat_amount": amount}
        elif kind==1:
            text=f"Montant de TVA: {amount}"; truth={"vat_amount": amount}
        elif kind==2:
            text=f"TVA à payer: {amount}"; truth={"vat_amount": amount}
        elif kind==3:
            text=f"Sales Tax: {amount}"; truth={}
        else:
            text=f"VAT Amount: {amount}\nVAT Amount: 999.99"; truth={}
        rows.append({"id":f"V4-{i+1:03d}", "dataset":"synthetic","text":text,"truth":truth})
    return rows

def run():
    return evaluate(cohort(),require_50=True)
