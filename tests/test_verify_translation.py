from pathlib import Path
import json
import subprocess
import sys
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

    def test_semantic_finds_untranslated_english_in_target_prose(self):
        report = self._report_for(
            "中文源内容。\n",
            "This sentence remains entirely in English and should be detected.\n",
        )
        self.assertTrue(any(f["rule_id"] == "P1-SEMANTIC" for f in report["findings"]))

    def test_semantic_ignores_source_language_quotations_and_blockquotes(self):
        for target in (
            '“This sentence remains entirely in English and should be allowed.”\n',
            '> This sentence remains entirely in English and should be allowed.\n',
        ):
            with self.subTest(target=target):
                report = self._report_for("中文源内容。\n", target)
                self.assertFalse(any(f["rule_id"] == "P1-SEMANTIC" for f in report["findings"]))

    def test_semantic_ignores_uppercase_abbreviation_combinations(self):
        report = self._report_for("中文源内容。\n", "API and GPU models\n")
        self.assertFalse(any(f["rule_id"] == "P1-SEMANTIC" for f in report["findings"]))

    def test_source_and_target_map_by_stable_numeric_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_dir, target_dir = root / "source", root / "target"
            source_dir.mkdir(); target_dir.mkdir()
            (source_dir / "01. source title.md").write_text("中文。\n", encoding="utf-8")
            (target_dir / "01. 中文标题.md").write_text("中文。\n", encoding="utf-8")
            report = verify_chapter(source_dir, target_dir)
            self.assertEqual("PASS", report["status"])
            self.assertEqual(1, report["metrics"]["files"])

    def test_missing_or_duplicate_numeric_prefix_rejects_mapping(self):
        cases = ((["01. source.md", "02. source.md"], ["01. target.md"]),
                 (["01. first.md", "01. second.md"], ["01. target.md"]))
        for source_names, target_names in cases:
            with self.subTest(source_names=source_names):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory); source_dir, target_dir = root / "source", root / "target"
                    source_dir.mkdir(); target_dir.mkdir()
                    for name in source_names: (source_dir / name).write_text("中文。\n", encoding="utf-8")
                    for name in target_names: (target_dir / name).write_text("中文。\n", encoding="utf-8")
                    report = verify_chapter(source_dir, target_dir)
                    self.assertEqual("FAIL", report["status"])
                    self.assertTrue(any(f["rule_id"] == "P0-FILE-MAP" for f in report["findings"]))

        for mark in ",.:;?!":
            with self.subTest(mark=mark):
                report = self._report_for("中文源内容。\n", f"中文内容{mark}\n")
                self.assertTrue(any(f["rule_id"] == "P2-PUNCTUATION" for f in report["findings"]))

    def test_p2_ignores_fences_block_math_and_inline_math(self):
        target = "```python\n中文, code\n```\n\n$$\n中文, math\n$$\n\n中文$ x,y $内容\n"
        report = self._report_for(target, target)
        self.assertFalse(any(f["rule_id"].startswith("P2-") for f in report["findings"]))

    def test_spacing_flags_han_adjacent_ascii_letter_or_digit(self):
        report = self._report_for("中文源内容。\n", "中文AI内容\n中文2内容\n")
        self.assertTrue(any(f["rule_id"] == "P2-SPACING" for f in report["findings"]))

    def test_spacing_ignores_inline_code(self):
        target = "中文 `AI` 内容\n中文 `2` 内容\n"
        report = self._report_for(target, target)
        self.assertFalse(any(f["rule_id"] == "P2-SPACING" for f in report["findings"]))

    def test_cli_report_has_metadata_and_chapter_is_not_appended(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "01.md").write_text("中文。\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/verify_translation.py", "--source-dir", str(root),
                 "--target-dir", str(root), "--chapter", "09", "--metrics-only"],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(0, result.returncode)
            report = json.loads(result.stdout)
            self.assertEqual("09", report["chapter"])
            self.assertEqual([], report["findings"])
            self.assertIn("metrics", report)

    def test_cli_missing_directory_exits_two(self):
        result = subprocess.run(
            [sys.executable, "scripts/verify_translation.py", "--source-dir", "/missing", "--target-dir", "/missing"],
            check=False, capture_output=True, text=True,
        )
        self.assertEqual(2, result.returncode)
