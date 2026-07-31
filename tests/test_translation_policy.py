from pathlib import Path
import unittest

GUIDE = Path("zh/TRANSLATION_GUIDE.md")

class TranslationPolicyTests(unittest.TestCase):
    def test_guide_requires_source_coverage_and_allows_labelled_expansion(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("原文信息单元", text)
        self.assertIn("一一对应", text)
        self.assertIn("可以比原文更丰富", text)
        self.assertIn("补充说明", text)
        self.assertIn("译注", text)

if __name__ == "__main__":
    unittest.main()
