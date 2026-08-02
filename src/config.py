import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    DEFAULT_FEEDS = ["https://news.ycombinator.com/rss", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"]
    RSS_FEEDS = [f.strip() for f in os.getenv("RSS_FEEDS", ",".join(DEFAULT_FEEDS)).split(",") if f.strip()]
    MAX_PER_FEED = os.getenv("MAX_PER_FEED", "4")
    LANGUAGE = os.getenv("LANGUAGE", "zh")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

    @classmethod
    def validate(cls):
        errors = []

        if cls.LANGUAGE not in {"zh", "en"}:
            errors.append("LANGUAGE must be either 'zh' or 'en'.")

        if not cls.RSS_FEEDS:
            errors.append("RSS_FEEDS must include at least one feed URL.")

        max_per_feed = _parse_positive_int(cls.MAX_PER_FEED)
        if max_per_feed is None:
            errors.append("MAX_PER_FEED must be a positive integer.")

        for feed_url in cls.RSS_FEEDS:
            if not _is_http_url(feed_url):
                errors.append(f"RSS feed URL is invalid: {feed_url}")

        if cls.WEBHOOK_URL and not _is_http_url(cls.WEBHOOK_URL):
            errors.append("WEBHOOK_URL must be a valid http(s) URL when provided.")

        return errors


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _parse_positive_int(value: str):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if parsed < 1:
        return None
    return parsed
