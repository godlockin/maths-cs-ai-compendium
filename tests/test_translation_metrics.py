import unittest

from scripts.verify_translation import prose_token_metrics


class TranslationMetricsTests(unittest.TestCase):
    def test_metrics_exclude_code_and_math_and_count_enhancements(self):
        metrics = prose_token_metrics(
            "English prose.\n\n$$x = y$$\n\n```python\nvalue = 1\n```\n",
            "中文正文。\n\n> **补充说明**: 中文扩展。\n\n$$x = y$$\n\n```python\nvalue = 1\n```\n",
        )
        self.assertGreater(metrics["source_tokens"], 0)
        self.assertGreater(metrics["target_tokens"], 0)
        self.assertGreater(metrics["enhancement_tokens"], 0)
        self.assertIn(metrics["tokenizer"], {"tiktoken", "estimate"})
        self.assertIn(metrics["confidence"], {"high", "low"})
        self.assertIsNotNone(metrics["ratio"])


if __name__ == "__main__":
    unittest.main()
