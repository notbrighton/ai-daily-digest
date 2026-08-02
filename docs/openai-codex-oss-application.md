# OpenAI Codex for Open Source Application Draft

Use this as a starting point when applying to the OpenAI Codex for Open Source program.

## Repository URL

`https://github.com/jieone/ai-daily-digest`

## Maintainer Role

I am the primary maintainer of AI Daily Digest. I created and maintain the project, review changes, manage the roadmap, improve reliability, and keep the automation workflow usable for developers and small teams.

## Project Description

AI Daily Digest is an open-source automation tool that turns noisy developer and technology RSS feeds into a daily intelligence briefing. It fetches configurable RSS sources, cleans and deduplicates entries, summarizes them with OpenAI when an API key is available, falls back gracefully when it is not, archives the result as Markdown, renders a static dashboard, and can publish automatically through GitHub Actions and GitHub Pages.

The goal is to help developers, maintainers, and indie builders keep up with AI and technology news without manually scanning many feeds every day.

## Why Codex Would Help

Codex would help with ongoing maintainer work such as:

- improving RSS extraction quality for sources that provide sparse metadata;
- adding tests for feed parsing, HTML rendering, configuration validation, and notification adapters;
- reviewing pull requests and catching regressions before daily automation runs;
- building a small CLI configuration flow for non-expert users;
- maintaining GitHub Actions workflows and release packaging;
- improving webhook integrations for Discord, Telegram, Feishu/Lark, and DingTalk.

## Current Maintenance Signals

- The project has a working end-to-end daily digest pipeline.
- It includes GitHub Actions automation for tests and scheduled publishing.
- It has a documented roadmap, contribution guide, issue templates, pull request template, and changelog.
- It includes a standard-library test suite covering core parsing and rendering behavior.

## Near-Term Roadmap

- Improve Hacker News extraction when RSS entries only expose comment placeholders.
- Add feed categories and per-source limits.
- Add provider-specific webhook payloads.
- Add historical views across archived digests.
- Publish a first tagged release and keep a regular changelog.

## Short Form Answer

I am the primary maintainer of AI Daily Digest, an open-source daily technology briefing generator for developers. The project automates RSS collection, AI-assisted summarization, Markdown archiving, static dashboard rendering, webhook notifications, and GitHub Pages publishing. Codex would help me maintain and improve the project by accelerating test coverage, PR review, RSS extraction improvements, release workflows, and user-facing configuration features.
