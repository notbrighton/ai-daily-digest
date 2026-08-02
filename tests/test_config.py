import unittest

from src.config import Config


class ConfigValidationTests(unittest.TestCase):
    def test_validate_accepts_default_config(self):
        self.assertEqual(Config.validate(), [])

    def test_validate_rejects_invalid_language_and_feed(self):
        class BadConfig(Config):
            LANGUAGE = "fr"
            RSS_FEEDS = ["not-a-url"]
            MAX_PER_FEED = "0"
            WEBHOOK_URL = "ftp://example.com/hook"

        errors = BadConfig.validate()

        self.assertTrue(any("LANGUAGE" in error for error in errors))
        self.assertTrue(any("RSS feed URL is invalid" in error for error in errors))
        self.assertTrue(any("MAX_PER_FEED" in error for error in errors))
        self.assertTrue(any("WEBHOOK_URL" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
