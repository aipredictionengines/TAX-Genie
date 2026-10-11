import os
import tempfile
import unittest
from tax_genie.api import create_app
from tax_genie.intake import IntakeStore

class TestAuthHardening(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=IntakeStore(self.tmp.name+"/db.sqlite",os.urandom(32))
    def tearDown(self):
        self.tmp.cleanup()
    def test_repeated_character_secret_rejected(self):
        with self.assertRaises(ValueError):
            create_app(store=self.store,tenant_tokens={"x":"A"*48})
    def test_space_or_colon_secret_rejected(self):
        with self.assertRaises(ValueError):
            create_app(store=self.store,tenant_tokens={"x":"a2345678"*5+" "})
    def test_duplicate_secret_rejected(self):
        key="9a80b71f42ce563d9a80b71f42ce563d"
        with self.assertRaises(ValueError):
            create_app(store=self.store,tenant_tokens={"x":key,"y":key})
    def test_reasonable_secret_accepted(self):
        create_app(store=self.store,tenant_tokens={"x":"0123456789abcdef0123456789abcdefA"})
if __name__=="__main__": unittest.main()
