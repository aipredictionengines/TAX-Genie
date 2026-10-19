import hashlib
import json
import unittest

from tax_genie.fixture_review_packet import (
    PACKET_VERSION, REVIEW_FIELDS, build_blind_review_packet,
)
from tax_genie.quality_cohort_v1 import make_quality_cohort


class TestBlindReviewPacket(unittest.TestCase):
    def test_14_cases_and_stable_hash(self):
        packet = build_blind_review_packet()
        self.assertEqual(packet["version"], PACKET_VERSION)
        self.assertEqual(len(packet["cases"]), 14)
        self.assertEqual(len({case["case_id"] for case in packet["cases"]}), 14)
        self.assertEqual(packet, build_blind_review_packet())
        canonical = {k: packet[k] for k in (
            "version", "source", "review_fields", "cases"
        )}
        data = json.dumps(canonical, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")).encode("utf-8")
        self.assertEqual(hashlib.sha256(data).hexdigest(),
                         packet["packet_sha256"])
        self.assertEqual(tuple(packet["review_fields"]), REVIEW_FIELDS)

    def test_no_expectations_answer_key_or_prior_extraction(self):
        packet = build_blind_review_packet()
        for case in packet["cases"]:
            self.assertEqual(set(case), {"case_id", "source_text"})
            self.assertTrue(case["source_text"].startswith("Invoice Number:"))
        self.assertEqual(
            packet["review_status"], "PENDING_EXTERNAL_REVIEW"
        )
        self.assertNotIn("semantic_truth", str(packet))
        self.assertNotIn("supported_expected", str(packet))
        self.assertNotIn("required_review_flags", str(packet))
        self.assertNotIn("refund_eligibility", str(packet))

    def test_packet_contains_only_authored_synthetic_source(self):
        rows = make_quality_cohort()
        packet = build_blind_review_packet()
        self.assertEqual(
            [(x["id"], x["text"]) for x in rows],
            [(x["case_id"], x["source_text"]) for x in packet["cases"]],
        )


if __name__ == "__main__":
    unittest.main()
