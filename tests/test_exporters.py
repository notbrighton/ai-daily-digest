import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from src.exporters.html import list_digest_archives, markdown_to_html


class HtmlExporterTests(unittest.TestCase):
    def test_markdown_to_html_wraps_articles_and_links(self):
        markdown = """# AI Daily Digest

### 1. [Example](https://example.com?a=1&b=2)
- **来源**: Example Feed
- **时间**: Today
- **摘要**: A short **summary**.
- **核心洞察**: Useful signal.
"""

        html = markdown_to_html(markdown)

        self.assertIn('<article class="digest-article">', html)
        self.assertIn('href="https://example.com?a=1&amp;b=2"', html)
        self.assertIn('<p class="article-meta"><strong>时间</strong>: Today</p>', html)
        self.assertIn('<strong>summary</strong>', html)
        self.assertIn('<div class="key-takeaway"><strong>核心洞察</strong>: Useful signal.</div>', html)

    def test_markdown_to_html_escapes_raw_html(self):
        html = markdown_to_html("### <script>alert(1)</script>\nPlain text")

        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)

    def test_list_digest_archives_returns_recent_files_first(self):
        with TemporaryDirectory() as temp_dir:
            archive_dir = Path(temp_dir)
            (archive_dir / "digest_20260802.md").write_text("# One", encoding="utf-8")
            (archive_dir / "digest_20260804.md").write_text("# Three", encoding="utf-8")
            (archive_dir / "notes.md").write_text("skip", encoding="utf-8")

            archives = list_digest_archives(str(archive_dir))

        self.assertEqual(archives[0]["label"], "2026-08-04")
        self.assertTrue(archives[0]["href"].endswith("digest_20260804.md"))
        self.assertEqual(len(archives), 2)


if __name__ == "__main__":
    unittest.main()
