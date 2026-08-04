import html
import re
import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def render_inline(markdown: str) -> str:
    pieces = []
    cursor = 0

    def link_repl(match):
        text = html.escape(match.group(1), quote=False)
        url = html.escape(match.group(2), quote=True)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

    for match in re.finditer(r'\[(.*?)\]\((.*?)\)', markdown):
        pieces.append(html.escape(markdown[cursor:match.start()], quote=True))
        pieces.append(link_repl(match))
        cursor = match.end()
    pieces.append(html.escape(markdown[cursor:], quote=True))

    escaped = "".join(pieces)
    escaped = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', escaped)
    return escaped

def markdown_to_html(md_text: str) -> str:
    parts = []
    article_open = False

    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            continue

        if line.startswith("## "):
            if article_open:
                parts.append("</article>")
                article_open = False
            parts.append(f'<h2 class="section-title">{render_inline(line[3:])}</h2>')
            continue

        if line.startswith("### "):
            if article_open:
                parts.append("</article>")
            parts.append('<article class="digest-article">')
            article_open = True
            parts.append(f'<h3 class="article-title">{render_inline(line[4:])}</h3>')
            continue

        bullet_match = re.match(r'-\s+\*\*(来源|Source)\*\*:\s*(.*)', line)
        if bullet_match:
            parts.append(f'<p class="article-meta"><strong>{bullet_match.group(1)}</strong>: {render_inline(bullet_match.group(2))}</p>')
            continue

        bullet_match = re.match(r'-\s+\*\*(时间|Published)\*\*:\s*(.*)', line)
        if bullet_match:
            parts.append(f'<p class="article-meta"><strong>{bullet_match.group(1)}</strong>: {render_inline(bullet_match.group(2))}</p>')
            continue

        bullet_match = re.match(r'-\s+\*\*(摘要|Summary)\*\*:\s*(.*)', line)
        if bullet_match:
            parts.append(f'<p class="article-summary"><strong>{bullet_match.group(1)}</strong>: {render_inline(bullet_match.group(2))}</p>')
            continue

        bullet_match = re.match(r'-\s+\*\*(核心洞察|Key Takeaway)\*\*:\s*(.*)', line)
        if bullet_match:
            parts.append(f'<div class="key-takeaway"><strong>{bullet_match.group(1)}</strong>: {render_inline(bullet_match.group(2))}</div>')
            continue

        if line.startswith("- "):
            parts.append(f'<p class="article-summary">{render_inline(line[2:])}</p>')
            continue

        parts.append(f'<p class="article-summary">{render_inline(line)}</p>')

    if article_open:
        parts.append("</article>")

    return "\n".join(parts)

def list_digest_archives(archive_dir: str = "digests", limit: int = 7):
    archives = []
    for path in sorted(Path(archive_dir).glob("digest_*.md"), reverse=True):
        date_match = re.search(r'digest_(\d{4})(\d{2})(\d{2})\.md$', path.name)
        if not date_match:
            continue
        year, month, day = date_match.groups()
        archives.append({
            "label": f"{year}-{month}-{day}",
            "href": f"{archive_dir}/{path.name}",
        })
        if len(archives) >= limit:
            break
    return archives

def export_html(md_content: str, articles_count: int, feeds_count: int, template_dir: str = "templates", output_path: str = "index.html", archive_dir: str = "digests") -> str:
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("index.html.jinja2")
    
    content_html = markdown_to_html(md_content)
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    archives = list_digest_archives(archive_dir)
    
    rendered_html = template.render(
        date_str=date_str,
        articles_count=articles_count,
        feeds_count=feeds_count,
        content_html=content_html,
        archives=archives
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    return output_path
