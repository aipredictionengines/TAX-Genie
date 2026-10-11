import unittest
from tax_genie.holdout_v4 import cohort,run

class TestHoldoutV4(unittest.TestCase):
    def test_cohort_frozen_and_unique(self):
        rows=cohort()
        self.assertEqual(len(rows),50)
        self.assertEqual(len({x["id"] for x in rows}),50)
        self.assertEqual(rows,cohort())
    def test_measurements_without_tuning(self):
        result=run()["per_field"]["synthetic"]["vat_amount"]
        self.assertEqual((result["tp"],result["fp"],result["fn"],result["tn"]),(20,0,10,20))
        self.assertEqual(result["precision"],1.0)
        self.assertEqual(result["recall"],0.6667)
if __name__=="__main__": unittest.main()
