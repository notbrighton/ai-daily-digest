import datetime
from typing import List, Dict
from openai import OpenAI
from src.config import Config

def _trim_text(text: str, limit: int) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."

def _fallback_digest(articles: List[Dict[str, str]], language: str) -> str:
    digest = f"# 🤖 AI Daily Digest - {datetime.date.today()}\n\n"

    for i, item in enumerate(articles, 1):
        title = item.get("title", "Untitled")
        link = item.get("link", "")
        source = item.get("source", "RSS Feed")
        published = item.get("published", "")
        summary = item.get("summary", "")

        digest += f"### {i}. [{title}]({link})\n"

        if language == "zh":
            digest += f"- **来源**: {source}\n"
            if published:
                digest += f"- **时间**: {published}\n"
            if summary:
                digest += f"- **摘要**: {_trim_text(summary, 220)}\n"
                digest += "- **核心洞察**: 这条内容值得关注，建议结合原文判断其对产品、工程或行业趋势的实际影响。\n\n"
            else:
                digest += "- **摘要**: 原始 RSS 未提供摘要，请打开链接阅读全文。\n"
                digest += "- **核心洞察**: 当前仅能确认标题和来源，后续可通过增强抓取获得更完整判断。\n\n"
        else:
            digest += f"- **Source**: {source}\n"
            if published:
                digest += f"- **Published**: {published}\n"
            if summary:
                digest += f"- **Summary**: {_trim_text(summary, 220)}\n"
                digest += "- **Key Takeaway**: Worth reviewing in context to understand its practical impact on products, engineering, or market direction.\n\n"
            else:
                digest += "- **Summary**: The source RSS feed did not provide a summary. Open the link to read the full article.\n"
                digest += "- **Key Takeaway**: Only the title and source are available for now; richer extraction can improve future analysis.\n\n"

    return digest

def summarize_articles(articles: List[Dict[str, str]]) -> str:
    if not articles:
        return "No articles fetched today."

    target_lang = "Chinese (中文)" if Config.LANGUAGE == "zh" else "English"
    
    # Prompt construction
    prompt = f"Please summarize the following tech articles into a structured, highly engaging daily digest in {target_lang}.\n"
    prompt += "Format requirements:\n"
    prompt += "- For EACH article, output an `### [Article Title](Link)` heading.\n"
    prompt += "- Include a 2-sentence **Summary**.\n"
    prompt += "- Include a **Key Takeaway** (Core insight or impact).\n\n"
    
    for i, item in enumerate(articles, 1):
        summary = item.get("summary") or "No summary provided by the source feed."
        published = item.get("published") or "Unknown"
        prompt += f"{i}. [{item['source']}] {item['title']}\n   Published: {published}\n   URL: {item['link']}\n   Content: {summary}\n\n"

    api_key = Config.OPENAI_API_KEY
    if not api_key or api_key == "your_openai_api_key_here":
        print("💡 No valid OPENAI_API_KEY detected. Using intelligent fallback generator...")
        return _fallback_digest(articles, Config.LANGUAGE)

    try:
        client = OpenAI(api_key=api_key, base_url=Config.OPENAI_BASE_URL)
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an elite AI tech editor and analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ OpenAI API Call Failed: {e}. Falling back to standard mode.")
        return _fallback_digest(articles, Config.LANGUAGE)
