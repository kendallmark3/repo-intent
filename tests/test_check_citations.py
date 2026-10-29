"""Tests for tools/check_citations.py. Run: python3 -m unittest discover -s tests"""
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_citations as cc  # noqa: E402

LEDGER_HEADER = (
    "## 15. Claims Ledger\n\n"
    "| ID | Claim | Class | Strength | Confidence | Evidence | Verification | Caveat |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


class CheckCitationsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        (self.repo / "src").mkdir(parents=True)
        (self.repo / "src" / "server.py").write_text(
            "import app\n\ndef main():\n    app.run(port=8080)\n"
        )
        (self.repo / "README.md").write_text("# Demo\nA demo service.\n")

    def tearDown(self):
        self.tmp.cleanup()

    def report(self, body: str, rows: str) -> Path:
        p = Path(self.tmp.name) / "REPORT.md"
        p.write_text(textwrap.dedent(body) + "\n" + LEDGER_HEADER + textwrap.dedent(rows))
        return p

    def test_valid_report_passes(self):
        r = self.report(
            "The service starts in `src/server.py:L3-L4#main` [C-001].",
            "| C-001 | `main` starts the app | OBSERVED | DIRECT | HIGH | `src/server.py:L3-L4#main` | VERIFIED | none |\n"
            "| C-002 | Production host | UNKNOWN | INSUFFICIENT | LOW | none in repo | VERIFIED | needs ops |\n",
        )
        res = cc.check_report(r, self.repo)
        self.assertEqual(res.errors, [])
        self.assertEqual(res.claims, 2)

    def test_missing_file_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `src/nope.py` | VERIFIED | - |\n")
        self.assertTrue(any("does not exist" in e for e in cc.check_report(r, self.repo).errors))

    def test_line_past_eof_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `src/server.py:L90` | VERIFIED | - |\n")
        self.assertTrue(any("past end of file" in e for e in cc.check_report(r, self.repo).errors))

    def test_symbol_not_in_range_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `src/server.py:L1#main` | VERIFIED | - |\n")
        self.assertTrue(any("symbol 'main' not found" in e for e in cc.check_report(r, self.repo).errors))

    def test_observed_without_evidence_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | trust me | VERIFIED | - |\n")
        self.assertTrue(any("no evidence citation" in e for e in cc.check_report(r, self.repo).errors))

    def test_body_claim_missing_from_ledger_is_error(self):
        r = self.report("x [C-001] and [C-009]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md` | VERIFIED | - |\n")
        self.assertTrue(any("C-009" in e for e in cc.check_report(r, self.repo).errors))

    def test_bad_vocabulary_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | PROBABLY | DIRECT | HIGH | `README.md` | VERIFIED | - |\n")
        self.assertTrue(any("class 'PROBABLY'" in e for e in cc.check_report(r, self.repo).errors))

    def test_path_escape_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `../../etc/passwd` | VERIFIED | - |\n")
        self.assertTrue(any("escapes" in e for e in cc.check_report(r, self.repo).errors))

    def test_numeric_confidence_warns(self):
        r = self.report("We are 90% confident [C-001].", "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md` | VERIFIED | - |\n")
        res = cc.check_report(r, self.repo)
        self.assertEqual(res.errors, [])
        self.assertTrue(any("Rule 13" in w for w in res.warnings))

    def test_plain_inline_code_is_not_a_citation(self):
        self.assertEqual(cc.parse_citations("Use `UNKNOWN` and `HIGH`."), [])

    def test_missing_ledger_is_error(self):
        p = Path(self.tmp.name) / "R.md"
        p.write_text("no ledger here")
        self.assertTrue(any("ledger table not found" in e for e in cc.check_report(p, self.repo).errors))


if __name__ == "__main__":
    unittest.main()
