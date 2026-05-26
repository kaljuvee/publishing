#!/usr/bin/env python3
"""
Playwright MCP browser workflow for OpenReview registration verification.

This script is NOT run directly — it documents the Playwright MCP commands
that Claude Code uses to visually verify registration status.

Usage with Claude Code:
    claude -p "Use Playwright to log into OpenReview and check my registration status. \
               Take screenshots and save them to screenshots/"

The workflow:
    1. Navigate to OpenReview login page
    2. Fill in credentials from .credentials/.env
    3. Navigate to the author console / submission page
    4. Take screenshots of registration status
    5. Save screenshots to screenshots/ directory

Playwright MCP tools used:
    - browser_navigate: Go to URLs
    - browser_snapshot: Read page structure (accessibility tree)
    - browser_fill_form: Fill login form
    - browser_click: Click buttons/links
    - browser_take_screenshot: Capture page state to screenshots/
"""

# URLs for the workflow
URLS = {
    "login": "https://openreview.net/login",
    "profile": "https://openreview.net/profile",
    "author_console": "https://openreview.net/group?id=aclweb.org/ACL/ARR/2026/May/Authors",
    "submission": "https://openreview.net/forum?id=eNnEx8x2CH",
    "registration_form": (
        "https://openreview.net/forum?id=eNnEx8x2CH"
        "&noteId=wtEpVpRryA"
        "&referrer=%5BAuthor%20Console%5D"
        "(%2Fgroup%3Fid%3Daclweb.org%2FACL%2FARR%2F2026%2FMay%2FAuthors%23author-tasks)"
    ),
}
