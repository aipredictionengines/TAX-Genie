import unittest
from tax_genie.invoice_evidence import extract_invoice_evidence

class TestParserGuardrails(unittest.TestCase):
    def test_explicit_french_vat_label(self):
        r=extract_invoice_evidence("Taxe sur valeur ajoutée 14.25")
        self.assertEqual(r["fields"]["vat_amount"]["value"],"14.25")
    def test_generic_tax_is_not_vat(self):
        r=extract_invoice_evidence("Tax Amount: 88.00")
        self.assertNotIn("vat_amount",r["fields"])
    def test_conflicting_explicit_vat_values(self):
        r=extract_invoice_evidence("VAT Amount: 10.00\nTVA montant: 11.00")
        self.assertNotIn("vat_amount",r["fields"])
        self.assertIn("CONFLICTING_VAT_AMOUNT",r["review_flags"])
    def test_vat_exceeds_invoice_total(self):
        r=extract_invoice_evidence("VAT Amount: 101.00\nInvoice Total: 100.00")
        self.assertIn("VAT_EXCEEDS_TOTAL",r["review_flags"])

if __name__=="__main__": unittest.main()
