"""Synthetic comparator contract tests only — NOT an independent review."""
import copy
import unittest

from tax_genie.fixture_review_packet import build_blind_review_packet, REVIEW_FIELDS
from tax_genie.invoice_evidence import extract_invoice_evidence
from tax_genie.quality_cohort_v1 import make_quality_cohort
from tax_genie.review_adjudication import REVIEW_SCHEMA, compare_review_submission


def simulated_submission():
    """Use AUTHOR labels solely to exercise software. Never submit as external evidence."""
    packet = build_blind_review_packet()
    cases = []
    for row in make_quality_cohort():
        parser = extract_invoice_evidence(row["text"])
        decisions = {}
        for field in REVIEW_FIELDS:
            if field in row["supported_expected"]:
                decisions[field] = {
                    "status": "VALUE",
                    "value": row["supported_expected"][field],
                    "line": parser["fields"][field]["line"],
                }
            else:
                decisions[field] = {"status": "ABSTAIN", "reason": "Insufficient source support"}
        cases.append({
            "case_id": row["id"],
            "fields": decisions,
            "review_flags": list(row["required_review_flags"]),
        })
    return {
        "schema": REVIEW_SCHEMA,
        "packet_sha256": packet["packet_sha256"],
        "reviewer_role": "document_quality_reviewer",
        "review_date": "2026-10-19",
        "independence_declared": False,
        "cases": cases,
    }


class TestReviewAdjudication(unittest.TestCase):
    def test_simulation_never_verifies_independent_review(self):
        result = compare_review_submission(simulated_submission())
        self.assertEqual(result["synthetic_case_count"], 14)
        self.assertEqual(result["disagreement_count"], 0)
        self.assertFalse(result["independence_verified"])
        self.assertFalse(result["external_signoff_verified"])
        self.assertEqual(result["review_gate"], "PENDING_HUMAN_ADJUDICATION_AND_SIGNOFF")
        self.assertNotIn("FR12345678901", str(result))
        self.assertNotIn("20.00", str(result))

    def test_declared_independence_does_not_verify_independence(self):
        review = simulated_submission()
        review["independence_declared"] = True
        result = compare_review_submission(review)
        self.assertTrue(result["independence_declared"])
        self.assertFalse(result["independence_verified"])
        self.assertFalse(result["external_signoff_verified"])

    def test_refuse_wrong_digest_and_missing_case(self):
        review = simulated_submission()
        review["packet_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            compare_review_submission(review)
        review = simulated_submission()
        review["cases"].pop()
        with self.assertRaises(ValueError):
            compare_review_submission(review)

    def test_refuse_duplicate_case_and_extra_freeform_payload(self):
        review = simulated_submission()
        review["cases"][1]["case_id"] = review["cases"][0]["case_id"]
        with self.assertRaises(ValueError):
            compare_review_submission(review)
        review = simulated_submission()
        review["reviewer_name"] = "PRIVATE"
        with self.assertRaises(ValueError):
            compare_review_submission(review)

    def test_disagreement_without_leaking_expected_amounts(self):
        review = simulated_submission()
        review["cases"][0]["fields"]["vat_amount"]["value"] = "999.99"
        result = compare_review_submission(review)
        self.assertTrue(any(x["issue"] == "value_disagreement" for x in result["disagreements"]))
        self.assertFalse(result["external_signoff_verified"])
        self.assertNotIn("999.99", str(result))

    def test_out_of_range_provenance_and_extra_flag(self):
        review = simulated_submission()
        review["cases"][0]["fields"]["vat_amount"]["line"] = 999
        review["cases"][0]["review_flags"].append("REVIEWER_UNEXPECTED_FLAG")
        result = compare_review_submission(review)
        self.assertTrue(any(x["issue"] == "line_out_of_range" for x in result["disagreements"]))
        self.assertTrue(any(x["issue"] == "reviewer_added_flag" for x in result["disagreements"]))

    def test_missing_review_flag_is_disagreement(self):
        review = simulated_submission()
        target = next(x for x in review["cases"] if x["case_id"] == "QVAL-009")
        target["review_flags"].clear()
        result = compare_review_submission(review)
        self.assertTrue(any(x["issue"] == "missing_author_flag" for x in result["disagreements"]))

    def test_malformed_annotations_rejected(self):
        review = simulated_submission()
        review["cases"][0]["fields"]["vat_amount"]["line"] = True
        with self.assertRaises(ValueError):
            compare_review_submission(review)
        review = simulated_submission()
        review["cases"][0]["fields"]["vat_amount"] = {"status": "ABSTAIN", "reason": ""}
        with self.assertRaises(ValueError):
            compare_review_submission(review)
        review = simulated_submission()
        review["cases"][0]["review_flags"] = ["DUP", "DUP"]
        with self.assertRaises(ValueError):
            compare_review_submission(review)


if __name__ == "__main__":
    unittest.main()
