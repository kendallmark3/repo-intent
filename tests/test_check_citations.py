"""Tests for tools/check_citations.py. Run: python3 -m unittest discover -s tests"""
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_citations as cc  # noqa: E402

MGMT = (
    "## Management Summary\n- Where it is today: a demo [C-001].\n- Current credible radius: 2.\n"
    "- What's working: tests.\n- Attention areas: none yet.\n- Questions to settle before setting direction: owner.\n\n"
)
RADIUS = "".join(f"| {n} R | PARTIAL | C-001 |\n" for n in range(1, 6))
BRIEF = (
    MGMT + "## Architect Brief\n- A demo service [C-001].\n- Radius position:\n\n| Radius | Status | Basis |\n|---|---|---|\n"
    + RADIUS + "\n- Attention areas: x.\n- Smallest next step outward: y.\n\n## 1. Repository Identity\n"
)
VERIFY = "\n## 17. What I would verify before repeating this in an architecture meeting\n- Check C-001.\n"
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
        p.write_text(BRIEF + textwrap.dedent(body) + "\n" + LEDGER_HEADER + textwrap.dedent(rows) + VERIFY)
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

    def test_prose_inline_paths_and_versions_are_ignored(self):
        r = self.report(
            "Routes `/api/health` and `/` at version `0.2.0` via `Orchestrator.run` [C-001].",
            "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md` | VERIFIED | - |\n",
        )
        self.assertEqual(cc.check_report(r, self.repo).errors, [])

    def test_prose_citation_with_locator_is_checked(self):
        r = self.report("See `src/server.py:L99` [C-001].",
                        "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md` | VERIFIED | - |\n")
        self.assertTrue(any("past end of file" in e for e in cc.check_report(r, self.repo).errors))

    def test_symbol_may_contain_spaces(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `src/server.py:L4#app.run(port` | VERIFIED | - |\n")
        self.assertEqual(cc.check_report(r, self.repo).errors, [])
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md#A demo service` | VERIFIED | - |\n")
        self.assertEqual(cc.check_report(r, self.repo).errors, [])
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md#not in file` | VERIFIED | - |\n")
        self.assertTrue(any("not found" in e for e in cc.check_report(r, self.repo).errors))

    def test_non_path_token_in_ledger_evidence_is_error(self):
        r = self.report("x [C-001]", "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md`; `0.2.0` | VERIFIED | - |\n")
        self.assertTrue(any("`0.2.0`" in e for e in cc.check_report(r, self.repo).errors))

    def test_missing_ledger_is_error(self):
        p = Path(self.tmp.name) / "R.md"
        p.write_text("no ledger here")
        self.assertTrue(any("ledger table not found" in e for e in cc.check_report(p, self.repo).errors))


class StructureAndAbsenceTest(CheckCitationsTest):
    ROW = "| C-001 | c | OBSERVED | DIRECT | HIGH | `README.md` | VERIFIED | - |\n"

    def write(self, text):
        p = Path(self.tmp.name) / "S.md"
        p.write_text(text)
        return cc.check_report(p, self.repo).errors

    def test_missing_brief_is_error(self):
        errs = self.write(MGMT + "## 1. Repository Identity\nx [C-001]\n" + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("missing '## Architect Brief'" in e for e in errs))

    def test_brief_below_section_one_is_error(self):
        errs = self.write(MGMT + "## 1. Repository Identity\n## Architect Brief\n- x [C-001]\n" + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("above section 1" in e for e in errs))

    def test_long_brief_is_error(self):
        long_brief = MGMT + "## Architect Brief\n" + ("word " * 401) + "[C-001]\n## 1. Repository Identity\n"
        errs = self.write(long_brief + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("max 400" in e for e in errs))

    def test_missing_management_summary_is_error(self):
        errs = self.write(BRIEF.replace(MGMT, "") + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("missing '## Management Summary'" in e for e in errs))

    def test_management_summary_below_brief_is_error(self):
        body = BRIEF.replace(MGMT, "").replace("## 1. Repository Identity\n", MGMT + "## 1. Repository Identity\n")
        errs = self.write(body + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("above the Architect Brief" in e for e in errs))

    def test_management_summary_rules(self):
        bad = MGMT.replace("a demo [C-001]", "see `src/server.py` [C-001] " + "word " * 150).replace("What's working: tests.\n", "")
        errs = self.write(BRIEF.replace(MGMT, bad) + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("max 150" in e for e in errs))
        self.assertTrue(any("plain language" in e for e in errs))
        self.assertTrue(any("'working'" in e for e in errs))

    def test_radius_table_rules(self):
        body = BRIEF.replace("| 5 R | PARTIAL |", "| 5 R | GREAT |").replace("| 3 R | PARTIAL | C-001 |\n", "")
        errs = self.write(body + LEDGER_HEADER + self.ROW + VERIFY)
        self.assertTrue(any("missing Radius 3" in e for e in errs))
        self.assertTrue(any("Radius 5 status 'GREAT'" in e for e in errs))

    def test_indented_radius_table_is_parsed(self):
        body = BRIEF.replace(RADIUS, "".join("  " + line + "\n" for line in RADIUS.splitlines()))
        self.assertEqual(self.write(body + LEDGER_HEADER + self.ROW + VERIFY), [])

    def test_radius_out_of_scope_is_valid(self):
        body = BRIEF.replace("| 5 R | PARTIAL |", "| 5 R | OUT OF SCOPE |")
        self.assertEqual(self.write(body + LEDGER_HEADER + self.ROW + VERIFY), [])

    def test_loaded_language_is_error_outside_code(self):
        r = self.report("The config is a sloppy mess [C-001]. `hack` in code is fine.", self.ROW)
        errs = cc.check_report(r, self.repo).errors
        self.assertTrue(any("'sloppy'" in e for e in errs))
        self.assertTrue(any("'mess'" in e for e in errs))
        self.assertFalse(any("'hack'" in e for e in errs))

    def test_missing_verify_section_is_error(self):
        errs = self.write(BRIEF + LEDGER_HEADER + self.ROW)
        self.assertTrue(any("verify before repeating" in e.lower() for e in errs))

    def test_verify_section_without_claim_ids_is_error(self):
        errs = self.write(BRIEF + LEDGER_HEADER + self.ROW + "\n## 17. What I would verify before repeating this\n- stuff\n")
        self.assertTrue(any("cites no claim IDs" in e for e in errs))

    def test_unscoped_absence_claim_is_error(self):
        r = self.report("x [C-001]", "| C-001 | The app has no authentication | OBSERVED | DIRECT | HIGH | `src/server.py` | VERIFIED | - |\n")
        errs = cc.check_report(r, self.repo).errors
        self.assertTrue(any("worded as a finding" in e for e in errs))
        self.assertTrue(any("Search scope:" in e for e in errs))
        self.assertTrue(any("cannot have DIRECT" in e for e in errs))

    def test_scoped_absence_claim_passes(self):
        r = self.report("x [C-001]", "| C-001 | No authentication was found on routes in `src/server.py` | OBSERVED | CORROBORATED | MEDIUM | `src/server.py` | VERIFIED | Search scope: full read of src/server.py; a gateway could add auth |\n")
        self.assertEqual(cc.check_report(r, self.repo).errors, [])

    def test_absence_rule_skips_unknown_claims(self):
        r = self.report("x [C-001]", "| C-001 | Never deployed | UNKNOWN | INSUFFICIENT | LOW | none | VERIFIED | - |\n")
        self.assertEqual(cc.check_report(r, self.repo).errors, [])


if __name__ == "__main__":
    unittest.main()
