# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

OpenReview Registration Agent for ACL Rolling Review (ARR) May 2026, targeting EMNLP 2026. Python CLI that checks author profiles, tracks registration form completion, and provides a dashboard via the OpenReview API.

## Commands

```bash
uv pip install -r requirements.txt          # install deps (uses uv-managed .venv)
python openreview_agent.py status           # full dashboard (single API session)
python openreview_agent.py profiles         # author profile check
python openreview_agent.py submission       # paper details
python openreview_agent.py registration     # form completion per author
python openreview_agent.py deadline         # time remaining
python openreview_agent.py guide            # recommended form answers
python openreview_agent.py browse           # Playwright MCP instructions
```

No test suite exists. Verify changes by running `python openreview_agent.py status`.

## Architecture

`openreview_agent.py` is the CLI entry point. Each `cmd_*` function is a subcommand. The `status` command creates one `OpenReviewClient` and passes it via `args.client` to avoid repeated logins (OpenReview rate-limits login to 3 requests per minute window).

`config.py` holds all static configuration: venue/forum/submission IDs, the 8-author list with OpenReview profile IDs (`~Name_N` format), and recommended form answers. Authors are looked up by `openreview_id` first, falling back to `email`.

`browse.py` is documentation-only — lists URLs for Playwright MCP visual verification workflows. Not imported anywhere.

## Non-obvious patterns

- **OpenReview API returns inconsistent types**: `get_profiles()` returns a dict when given emails, a list when given tilde-IDs. `cmd_profiles` normalizes both into `profiles_by_id` before lookup.
- **Registration detection uses 4 invitation patterns** plus a forum-reply fallback, because the exact invitation path varies by venue. Even so, the API typically returns 0 notes due to permission scoping — use Playwright for reliable visual verification.
- **Credentials**: loaded from `.credentials/.env` via python-dotenv, falling back to environment variables. The `.credentials/` directory is gitignored.
- **Screenshots**: `screenshots/` directory tracks `.gitkeep` but gitignores `*.png` and `*.jpeg` — Playwright captures go here.
- **Deadline timezone**: hardcoded as BST (UTC+1) since the ARR deadline is defined in UK time.
