import unittest
from io import BytesIO
from pypdf import PdfWriter
from tax_genie.pdf_isolation import parse_pdf_bounded

class TestPDFIsolation(unittest.TestCase):
    def test_blank_synthetic_pdf(self):
        buf=BytesIO(); pdf=PdfWriter(); pdf.add_blank_page(width=200,height=300); pdf.write(buf)
        r=parse_pdf_bounded(buf.getvalue(), timeout=10)
        self.assertEqual(r["pages"],1)
        self.assertEqual(r["text"],"")
    def test_non_pdf_rejected(self):
        with self.assertRaises(ValueError): parse_pdf_bounded(b"not a pdf")
    def test_bad_timeout_rejected(self):
        with self.assertRaises(ValueError): parse_pdf_bounded(b"%PDF-x",timeout=0)
    def test_bad_pdf_rejected(self):
        with self.assertRaises(ValueError): parse_pdf_bounded(b"%PDF-invalid",timeout=10)
if __name__=="__main__": unittest.main()
