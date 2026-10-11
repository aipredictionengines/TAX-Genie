import unittest
from tax_genie.holdout_v2 import frozen_holdout_v2, run_holdout_v2

class TestFrozenProspectiveHoldout(unittest.TestCase):
    def test_50_distinct_cases(self):
        cases=frozen_holdout_v2()
        self.assertEqual(len(cases),50)
        self.assertEqual(len({c["id"] for c in cases}),50)
        self.assertEqual({c["dataset"] for c in cases},{"synthetic"})
    def test_results_and_no_false_vat_claims(self):
        result=run_holdout_v2()
        v=result["per_field"]["synthetic"]["vat_amount"]
        self.assertEqual((v["tp"],v["fp"],v["fn"],v["tn"]),(20,0,10,20))
        self.assertEqual(v["precision"],1.0)
        self.assertEqual(v["recall"],0.6667)
    def test_cohort_reproducible(self):
        self.assertEqual(frozen_holdout_v2(),frozen_holdout_v2())
if __name__=="__main__":
    unittest.main()
