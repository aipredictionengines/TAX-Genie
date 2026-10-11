import unittest
from tax_genie.security_controls import RateLimiter,Scanner,verified_scan,audit_digest
class TestControls(unittest.TestCase):
    def test_rate_limit(self):
        limiter=RateLimiter(limit=2)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))
        self.assertTrue(limiter.allow("b"))
    def test_scanner_fail_closed(self):
        self.assertFalse(verified_scan(Scanner(),b"synthetic"))
    def test_explicit_clean_scanner(self):
        class Fake:
            def scan(self,b):return True
        self.assertTrue(verified_scan(Fake(),b"synthetic"))
    def test_deterministic_event_digest(self):
        d=audit_digest("a","case","CREATED",b"secret")
        self.assertEqual(d,audit_digest("a","case","CREATED",b"secret"))
        self.assertNotEqual(d,audit_digest("b","case","CREATED",b"secret"))
if __name__=="__main__":unittest.main()
