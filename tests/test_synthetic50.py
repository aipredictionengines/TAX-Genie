import unittest
from tax_genie.synthetic50 import make_cohort, run

class TestSynthetic50(unittest.TestCase):
    def test_exactly_fifty_unique_synthetic_cases(self):
        rows=make_cohort()
        self.assertEqual(len(rows),50)
        self.assertEqual(len({row["id"] for row in rows}),50)
        self.assertEqual({row["dataset"] for row in rows},{"synthetic"})
    def test_deterministic(self):
        self.assertEqual(make_cohort(),make_cohort())
    def test_fixed_cohort_after_parser_improvement(self):
        result=run()
        self.assertEqual(result["total"],50)
        self.assertEqual(result["datasets"]["synthetic"]["count"],50)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["fn"],0)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["fp"],0)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["tp"],30)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["precision"],1.0)
        self.assertEqual(result["per_field"]["synthetic"]["vat_amount"]["recall"],1.0)

if __name__=="__main__": unittest.main()
