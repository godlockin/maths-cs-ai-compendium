from pathlib import Path
import tempfile
import unittest

from scripts.verify_translation import verify_chapter

ROOT = Path("tests/fixtures/translation_qa")
SOURCE = ROOT / "source"


class VerifyTranslationTests(unittest.TestCase):
    def _report_for(self, source_text: str, target_text: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_dir = root / "source"
            target_dir = root / "target"
            source_dir.mkdir()
            target_dir.mkdir()
            (source_dir / "01.md").write_text(source_text, encoding="utf-8")
            (target_dir / "01.md").write_text(target_text, encoding="utf-8")
            return verify_chapter(source_dir, target_dir, strict=False)

    def test_valid_target_passes_with_labelled_enhancements(self):
        report = verify_chapter(SOURCE, ROOT / "target_valid", strict=False)
        self.assertEqual("PASS", report["status"])
        self.assertEqual([], report["findings"])

    def test_formula_change_is_p0(self):
        report = verify_chapter(SOURCE, ROOT / "target_formula_changed", strict=False)
        self.assertTrue(any(f["rule_id"] == "P0-MATH" for f in report["findings"]))
        self.assertEqual("FAIL", report["status"])

    def test_missing_source_paragraph_is_p0(self):
        report = verify_chapter(SOURCE, ROOT / "target_missing_paragraph", strict=False)
        self.assertTrue(any(f["rule_id"] == "P0-SOURCE-COVERAGE" for f in report["findings"]))

    def test_inline_link_does_not_hide_missing_prose(self):
        report = verify_chapter(
            ROOT / "source_inline_link", ROOT / "target_inline_link", strict=False
        )
        self.assertTrue(any(f["rule_id"] == "P0-SOURCE-COVERAGE" for f in report["findings"]))

    def test_list_url_only_does_not_hide_missing_prose(self):
        report = self._report_for(
            "- Source item [source](https://example.com)\n",
            "- [target](https://example.com)\n",
        )
        self.assertTrue(any(f["rule_id"] == "P0-SOURCE-COVERAGE" for f in report["findings"]))

    def test_blockquote_url_only_does_not_hide_missing_prose(self):
        report = self._report_for(
            "> Source note [source](https://example.com)\n",
            "> [target](https://example.com)\n",
        )
        self.assertTrue(any(f["rule_id"] == "P0-SOURCE-COVERAGE" for f in report["findings"]))

    def test_table_url_only_does_not_hide_missing_prose(self):
        report = self._report_for(
            "| Source item [source](https://example.com) |\n",
            "| [target](https://example.com) |\n",
        )
        self.assertTrue(any(f["rule_id"] == "P0-SOURCE-COVERAGE" for f in report["findings"]))

    def test_unlabelled_expansion_is_p1(self):
        report = verify_chapter(SOURCE, ROOT / "target_unlabelled_expansion", strict=False)
        self.assertTrue(any(f["rule_id"] == "P1-UNLABELLED-EXPANSION" for f in report["findings"]))

    def test_halfwidth_punctuation_warns_and_strict_fails(self):
        warning = verify_chapter(SOURCE, ROOT / "target_punctuation", strict=False)
        strict = verify_chapter(SOURCE, ROOT / "target_punctuation", strict=True)
        self.assertTrue(any(f["rule_id"] == "P2-PUNCTUATION" for f in warning["findings"]))
        self.assertEqual("PASS", warning["status"])
        self.assertEqual("FAIL", strict["status"])
