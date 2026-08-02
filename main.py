import sys
from src.config import Config
from src.fetchers.rss import fetch_rss_articles
from src.summarizer.llm import summarize_articles
from src.exporters.markdown import export_markdown
from src.exporters.html import export_html
from src.notifiers.webhook import send_webhook_notification

def main():
    print("=" * 50)
    print("🤖 Starting AI Daily Digest Builder")
    print("=" * 50)

    config_errors = Config.validate()
    if config_errors:
        print("⚠️ Configuration error:")
        for error in config_errors:
            print(f"  - {error}")
        sys.exit(1)

    # 1. Fetch RSS Feeds
    print(f"📡 Fetching RSS entries from {len(Config.RSS_FEEDS)} feeds...")
    articles = fetch_rss_articles(Config.RSS_FEEDS, max_per_feed=int(Config.MAX_PER_FEED))
    print(f"✅ Successfully fetched {len(articles)} articles.")

    if not articles:
        print("⚠️ No articles found. Exiting.")
        sys.exit(0)

    # 2. Generate LLM Digest
    print("🧠 Generating AI Daily Digest...")
    digest_md = summarize_articles(articles)

    # 3. Export Markdown Archive
    md_file = export_markdown(digest_md)
    print(f"📝 Markdown report saved to: {md_file}")

    # 4. Export HTML Page for GitHub Pages
    html_file = export_html(digest_md, len(articles), len(Config.RSS_FEEDS))
    print(f"🌐 HTML index page rendered to: {html_file}")

    # 5. Webhook Notification
    if Config.WEBHOOK_URL:
        send_webhook_notification(digest_md)

    print("=" * 50)
    print("🎉 AI Daily Digest execution completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
