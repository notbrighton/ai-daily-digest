# Changelog

All notable changes to AI Daily Digest will be documented here.

## 0.1.0 - 2026-08-02

### Added

- RSS-based tech news collection with configurable feed URLs.
- OpenAI-powered daily digest generation with a no-key fallback mode.
- Markdown archive export under `digests/`.
- Static HTML dashboard export for GitHub Pages.
- Optional generic webhook notification support.
- GitHub Actions workflow for daily automation.
- Standard-library test suite for RSS cleanup, fallback summaries, and HTML rendering.

### Improved

- HTML rendering now creates structured article blocks and escapes raw HTML.
- RSS cleanup filters low-value placeholders such as `Comments` and `Read more...`.
- README now includes a roadmap and contribution guidance.
