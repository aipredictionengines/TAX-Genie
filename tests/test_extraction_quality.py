import unittest
from tax_genie.quality_cohort_v1 import make_quality_cohort
from tax_genie.extraction_quality import evaluate_quality
from tax_genie.invoice_evidence import extract_invoice_evidence


class TestExtractionQuality(unittest.TestCase):
    def test_frozen_synthetic_cases_and_independent_truth(self):
        rows = make_quality_cohort()
        self.assertEqual(len(rows), 14)
        self.assertEqual(len({x["id"] for x in rows}), 14)
        self.assertEqual({x["dataset"] for x in rows}, {"synthetic"})
        self.assertEqual(make_quality_cohort(), rows)
        conflicted = next(x for x in rows if x["id"] == "QVAL-009")
        self.assertEqual(conflicted["semantic_truth"]["vat_amount"], "20.00")
        self.assertNotIn("vat_amount", conflicted["supported_expected"])

    def test_quality_gate_and_explicit_recall_limits(self):
        result = evaluate_quality(make_quality_cohort())
        self.assertTrue(result["passed"], result["failures"])
        self.assertEqual(result["total_cases"], 14)
        self.assertEqual(result["metrics"].get("unsafe_assertions", 0), 0)
        self.assertEqual(result["metrics"].get("missing_required_flags", 0), 0)
        self.assertEqual(result["metrics"].get("policy_violations", 0), 0)
        self.assertEqual(result["metrics"].get("safe_abstentions_on_known_truth"), 4)
        self.assertEqual(result["supported_exact_rate"], 1.0)
        self.assertLess(result["semantic_exact_coverage"], 1.0)
        self.assertNotIn("FR12345678901", str(result))
        self.assertNotIn("Invoice Number:", str(result))

    def test_rejects_real_data_and_duplicates(self):
        rows = make_quality_cohort()
        rows[0]["dataset"] = "consented_real"
        with self.assertRaises(ValueError):
            evaluate_quality(rows)
        rows = make_quality_cohort()
        rows[1]["id"] = rows[0]["id"]
        with self.assertRaises(ValueError):
            evaluate_quality(rows)

    def test_detects_unsafe_vat_assertion(self):
        def unsafe(text):
            result = extract_invoice_evidence(text)
            if "vat_amount" not in result["fields"]:
                result["fields"]["vat_amount"] = {
                    "value": "999.99", "line": 1, "method": "labeled_regex"
                }
            return result
        result = evaluate_quality(make_quality_cohort(), extractor=unsafe)
        self.assertFalse(result["passed"])
        self.assertGreater(result["metrics"].get("unsafe_assertions", 0), 0)

    def test_detects_unapproved_refund_decision(self):
        def reckless(text):
            result = extract_invoice_evidence(text)
            result["refund_eligibility"] = "APPROVED"
            result["recoverable_amount"] = "10.00"
            return result
        result = evaluate_quality(make_quality_cohort(), extractor=reckless)
        self.assertFalse(result["passed"])
        self.assertEqual(result["metrics"].get("policy_violations"), 14)


if __name__ == "__main__":
    unittest.main()
