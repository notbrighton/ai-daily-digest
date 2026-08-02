import unittest

from unittest.mock import Mock, patch

from src.fetchers.rss import clean_html, fetch_rss_articles, is_low_value_summary


class RssFetcherTests(unittest.TestCase):
    def test_clean_html_removes_tags_decodes_entities_and_normalizes_space(self):
        self.assertEqual(clean_html("<p>Hello&nbsp;<b>world</b></p>\nAgain"), "Hello world Again")

    def test_is_low_value_summary_detects_comment_placeholders(self):
        self.assertTrue(is_low_value_summary("Comments"))
        self.assertTrue(is_low_value_summary(" read more... "))
        self.assertFalse(is_low_value_summary("A useful article summary."))

    @patch("src.fetchers.rss.requests.get")
    def test_fetch_rss_articles_parses_response_content(self, mock_get):
        response = Mock()
        response.content = b"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Example Feed</title>
    <item>
      <title>Example Article</title>
      <link>https://example.com/article</link>
      <description><![CDATA[<p>Useful summary</p>]]></description>
      <pubDate>Sun, 02 Aug 2026 00:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>"""
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        articles = fetch_rss_articles(["https://example.com/feed.xml"])

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Example Article")
        self.assertEqual(articles[0]["summary"], "Useful summary")
        self.assertEqual(articles[0]["source"], "Example Feed")


if __name__ == "__main__":
    unittest.main()
