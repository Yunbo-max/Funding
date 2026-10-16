import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'skills/funding-autopilot/scripts/verify_grant_pdf.py'
spec = importlib.util.spec_from_file_location('verify_grant_pdf', MODULE)
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class GrantPdfTests(unittest.TestCase):
    def make_pdf(self, path: Path, lines, pages=1):
        try:
            from reportlab.pdfgen import canvas
        except ImportError:
            self.skipTest('reportlab not installed (test-fixture only)')
        pdf = canvas.Canvas(str(path))
        for n in range(pages):
            for i, line in enumerate(lines):
                pdf.drawString(60, 760 - 20 * i, line)
            pdf.showPage()
        pdf.save()

    def test_page_count_and_text_layer(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'draft.pdf'
            self.make_pdf(path, ['Funding research proposal with valid extractable text.'], pages=2)
            out = verify.verify_pdf(path, 1, ['research proposal'])
            self.assertEqual(out['status'], 'failed')
            self.assertTrue(any('pages' in problem for problem in out['issues']))

    def test_placeholders_are_not_ready(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'draft.pdf'
            self.make_pdf(path, ['Research proposal. [TO CONFIRM: host letter].'])
            out = verify.verify_pdf(path, 1, [])
            self.assertTrue(any('placeholder' in problem for problem in out['issues']))

    def test_good_mechanical_result_does_not_certify_visual(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'draft.pdf'
            self.make_pdf(path, ['Research proposal with enough readable text for verification.'])
            out = verify.verify_pdf(path, 1, ['Research proposal'])
            self.assertEqual(out['status'], 'mechanical_checks_passed_visual_review_required')
            self.assertTrue(out['visual_review_required'])

    def test_absent_pdf(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, 'does not exist'):
                verify.verify_pdf(Path(td) / 'missing.pdf', 1, [])


if __name__ == '__main__':
    unittest.main()
