"""Independent fixture families not reused by the original PAPER 50 cohort."""
import unittest
from tax_genie.paper50 import evaluate

def holdout():
    rows=[]
    for i in range(50):
        amt=f"{i+1}.50"
        mode=i%5
        # Five alternate layouts: supported French labels, English case variations,
        # unsupported one-line table, conflicting lines, and unlabeled values.
        if mode==0:
            text=f"TVA montant: {amt}\nDevise: EUR"
            truth={"vat_amount":amt,"currency":"EUR"}
        elif mode==1:
            text=f"vat total: {amt}"
            truth={"vat_amount":amt}
        elif mode==2:
            text=f"Taxe sur valeur ajoutée {amt}"
            truth={"vat_amount":amt}
        elif mode==3:
            text=f"VAT Amount: {amt}\nVAT Amount: 999.00"
            truth={}
        else:
            text=f"Tax Amount: {amt}"
            truth={"vat_amount":amt}
        rows.append({"id":f"H{i+1:03d}","dataset":"synthetic","text":text,"truth":truth})
    return rows

class TestIndependentHoldout(unittest.TestCase):
    def test_fifty_new_frozen_cases(self):
        result=evaluate(holdout(),require_50=True)
        self.assertEqual(result["total"],50)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["tp"],30)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["fn"],10)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["fp"],0)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["recall"],0.75)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["precision"],1.0)

if __name__=="__main__": unittest.main()
