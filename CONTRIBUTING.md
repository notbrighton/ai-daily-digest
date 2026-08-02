# Contributing to AI Daily Digest

Thanks for helping improve AI Daily Digest. This project is intentionally small and friendly to first-time contributors.

## Development Setup

```bash
git clone https://github.com/jieone/ai-daily-digest.git
cd ai-daily-digest
python -m pip install -r requirements.txt
cp .env.example .env
```

## Local Checks

Run tests before opening a pull request:

```bash
python -m unittest discover -s tests
```

Run the generator locally:

```bash
python main.py
```

## Good First Contributions

- Add or document useful RSS feeds.
- Improve fallback summaries when feeds provide sparse metadata.
- Add tests around edge cases in RSS parsing and HTML rendering.
- Improve webhook payload compatibility.
- Polish the generated dashboard while keeping it static-site friendly.

## Pull Request Guidelines

- Keep changes focused and easy to review.
- Include tests for behavior changes.
- Update README or `.env.example` when configuration changes.
- Do not commit `.env`, API keys, tokens, or generated cache files.
