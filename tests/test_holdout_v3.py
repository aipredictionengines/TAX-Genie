import unittest
from tax_genie.holdout_v3 import make_holdout_v3, run

class TestHoldoutV3(unittest.TestCase):
    def test_unique_frozen_50(self):
        items=make_holdout_v3()
        self.assertEqual(len(items),50)
        self.assertEqual(len({x["id"] for x in items}),50)
    def test_adversarial_synthetic_metrics(self):
        v=run()["per_field"]["synthetic"]["vat_amount"]
        self.assertEqual((v["tp"],v["fp"],v["fn"],v["tn"]),(20,0,10,20))
        self.assertEqual(v["recall"],0.6667)
        self.assertEqual(v["precision"],1.0)
if __name__=="__main__": unittest.main()
