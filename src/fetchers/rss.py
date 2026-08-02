import html
import re
import feedparser
import requests
from typing import List, Dict

def clean_html(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', '', text)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def is_low_value_summary(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in {"comments", "comment", "read more", "read more...", "..."}

def fetch_rss_articles(feed_urls: List[str], max_per_feed: int = 4) -> List[Dict[str, str]]:
    articles = []
    seen_links = set()

    for url in feed_urls:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "AI-Daily-Digest/0.1 (+https://github.com/jieone/ai-daily-digest)"},
                timeout=15,
            )
            response.raise_for_status()
            feed = feedparser.parse(response.content)

            if getattr(feed, "bozo", False):
                print(f"⚠️ Feed parser warning for {url}: {feed.bozo_exception}")

            for entry in feed.entries[:max_per_feed]:
                link = entry.get("link", "")
                if link in seen_links:
                    continue
                seen_links.add(link)
                
                title = clean_html(entry.get("title", "No Title"))
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                if is_low_value_summary(summary):
                    summary = ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "summary": summary[:400],
                    "source": feed.feed.get("title", "RSS Feed"),
                    "published": entry.get("published", "")
                })
        except Exception as e:
            print(f"⚠️ Error fetching feed {url}: {e}")
            
    return articles
