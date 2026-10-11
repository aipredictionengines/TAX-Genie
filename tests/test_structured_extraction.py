import unittest
from tax_genie.structured_extraction import parse_structured_text

class TestStructuredExtraction(unittest.TestCase):
    def test_explicit_aliases(self):
        r=parse_structured_text("VAT payable = 12.20\nTotal payable: 120.20\nInvoice currency = EUR")
        self.assertEqual(r["fields"]["vat_amount"]["value"],"12.20")
        self.assertEqual(r["fields"]["total_amount"]["value"],"120.20")
        self.assertEqual(r["fields"]["currency"]["value"],"EUR")
        self.assertEqual(r["refund_eligibility"],"UNDETERMINED")
    def test_ambiguous_tax_rejected(self):
        r=parse_structured_text("Tax: 20.00\nSales Tax: 21.00")
        self.assertNotIn("vat_amount",r["fields"])
    def test_conflicting_aliases_rejected(self):
        r=parse_structured_text("VAT payable: 12.00\nVAT due: 15.00")
        self.assertIn("CONFLICTING_VAT_AMOUNT",r["review_flags"])
        self.assertNotIn("vat_amount",r["fields"])
    def test_refuse_unlabelled(self):
        self.assertNotIn("vat_amount",parse_structured_text("EUR 200")["fields"])
if __name__=="__main__": unittest.main()
