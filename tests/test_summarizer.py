import unittest

from src.config import Config
from src.summarizer.llm import summarize_articles


class SummarizerTests(unittest.TestCase):
    def test_summarizer_fallback_handles_missing_source_summary(self):
        original_api_key = Config.OPENAI_API_KEY
        Config.OPENAI_API_KEY = ""
        try:
            digest = summarize_articles([
                {
                    "title": "Example",
                    "link": "https://example.com",
                    "source": "Example Feed",
                    "summary": "",
                    "published": "Today",
                }
            ])
        finally:
            Config.OPENAI_API_KEY = original_api_key

        self.assertIn("Example", digest)
        self.assertIn("原始 RSS 未提供摘要", digest)


if __name__ == "__main__":
    unittest.main()
