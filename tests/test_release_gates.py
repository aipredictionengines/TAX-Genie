import unittest
from tax_genie.release_gates import GATES,release_readiness
class TestReleaseGates(unittest.TestCase):
    def test_defaults_fail_closed(self):
        r=release_readiness()
        self.assertEqual(r["public_launch"],"BLOCKED")
        self.assertTrue(all(x["status"]=="BLOCKED" for x in r["gates"].values()))
    def test_no_self_certification(self):
        fake={g:{"approved":True,"reviewer":"self","evidence_reference":"claimed","verified_at":"2026-10-11"} for g in GATES}
        r=release_readiness(fake)
        self.assertEqual(r["public_launch"],"BLOCKED")
        self.assertTrue(all(x["status"]=="REVIEW_SUBMITTED" for x in r["gates"].values()))
if __name__=="__main__":
    unittest.main()
