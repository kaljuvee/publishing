#!/usr/bin/env python3
"""
OpenReview Registration Agent — ARR May 2026 / EMNLP 2026

Checks author profiles and registration status on OpenReview for the
submitted paper, and prints a dashboard with recommended form answers.

Usage:
    python openreview_agent.py status          # full dashboard
    python openreview_agent.py profiles        # check author profiles
    python openreview_agent.py submission      # check submission details
    python openreview_agent.py guide           # print form-filling guide
    python openreview_agent.py deadline        # time remaining until deadline
"""

import argparse
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from dotenv import load_dotenv
from tabulate import tabulate

import config

CREDENTIALS_PATH = Path(__file__).parent / ".credentials" / ".env"


def load_credentials():
    if CREDENTIALS_PATH.exists():
        load_dotenv(CREDENTIALS_PATH)
    username = os.getenv("OPENREVIEW_USERNAME")
    password = os.getenv("OPENREVIEW_PASSWORD")
    if not username or not password:
        print(
            "Error: OpenReview credentials not found.\n"
            f"Set OPENREVIEW_USERNAME and OPENREVIEW_PASSWORD in {CREDENTIALS_PATH}\n"
            "or as environment variables."
        )
        sys.exit(1)
    return username, password


def get_client():
    username, password = load_credentials()
    import openreview
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net",
        username=username,
        password=password,
    )
    return client


def cmd_profiles(args):
    """Check OpenReview profiles for all authors."""
    client = args.client if hasattr(args, "client") else get_client()
    import openreview
    rows = []

    lookup_ids = []
    for a in config.AUTHORS:
        if a.get("openreview_id"):
            lookup_ids.append(a["openreview_id"])
        elif a.get("email"):
            lookup_ids.append(a["email"])

    profiles_result = openreview.tools.get_profiles(client, ids_or_emails=lookup_ids) if lookup_ids else []
    profiles_by_id = {}
    if isinstance(profiles_result, dict):
        profiles_by_id = profiles_result
    elif isinstance(profiles_result, list):
        for p in profiles_result:
            if hasattr(p, "id"):
                profiles_by_id[p.id] = p
            if hasattr(p, "content"):
                for email_entry in p.content.get("emails", []):
                    profiles_by_id[email_entry] = p

    for author in config.AUTHORS:
        key = author.get("openreview_id") or author.get("email")
        if not key:
            rows.append([author["name"], "—", "No ID/email", "—", "—", "—"])
            continue
        profile = profiles_by_id.get(key)
        if profile:
            history = profile.content.get("history", [])
            affiliations = [
                h.get("institution", {}).get("name", "?")
                if isinstance(h.get("institution"), dict)
                else h.get("institution", "?")
                for h in history[:2]
            ]
            dblp = profile.content.get("dblp", "")
            semantic = profile.content.get("semanticScholar", "")
            rows.append([
                author["name"],
                author.get("openreview_id", ""),
                "Yes",
                ", ".join(affiliations) or "—",
                "Yes" if dblp else "No",
                "Yes" if semantic else "No",
            ])
        else:
            rows.append([author["name"], key, "No", "—", "—", "—"])

    headers = ["Author", "OpenReview ID", "Profile Found", "Affiliations", "DBLP", "Semantic Scholar"]
    print("\n=== Author Profile Check ===\n")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()


def cmd_submission(args):
    """Check submission details on OpenReview."""
    client = args.client if hasattr(args, "client") else get_client()
    submission_id = getattr(config, "SUBMISSION_ID", config.FORUM_ID)
    print(f"\n=== Submission Details (ID: {submission_id}) ===\n")
    try:
        notes = client.get_notes(forum=submission_id)
        if not notes:
            print("No notes found for this forum ID.")
            return
        submission = notes[0]
        content = submission.content
        title = content.get("title", {})
        if isinstance(title, dict):
            title = title.get("value", "?")
        print(f"Title:   {title}")
        authors_field = content.get("authors", {})
        if isinstance(authors_field, dict):
            authors_field = authors_field.get("value", [])
        if authors_field:
            print(f"Authors: {', '.join(authors_field)}")
        venue = content.get("venue", {})
        if isinstance(venue, dict):
            venue = venue.get("value", "?")
        if venue:
            print(f"Venue:   {venue}")
        print(f"Forum:   https://openreview.net/forum?id={submission_id}")
    except Exception as e:
        print(f"Could not fetch submission: {e}")
    print()


def cmd_registration(args):
    """Check author registration form completion status."""
    client = args.client if hasattr(args, "client") else get_client()
    print(f"\n=== Author Registration Status ===\n")
    print(f"Venue: {config.VENUE_ID}")
    print(f"Form:  {config.FORM_URL}\n")

    invitation_patterns = [
        f"{config.VENUE_ID}/Authors/-/Registration",
        f"{config.VENUE_ID}/-/Author_Registration",
        f"{config.VENUE_ID}/Authors/-/Author_Registration",
        f"{config.VENUE_ID}/Authors/-/Submitted_Author_Form",
    ]

    registration_notes = []
    for pattern in invitation_patterns:
        try:
            notes = client.get_all_notes(invitation=pattern)
            registration_notes.extend(notes)
        except Exception:
            pass

    if not registration_notes:
        try:
            replies = client.get_all_notes(forum=config.FORUM_ID)
            registration_notes = [
                n for n in replies
                if n.id != config.FORUM_ID
                and ("registration" in str(n.invitation).lower()
                     or "author_form" in str(n.invitation).lower()
                     or "submitted_author" in str(n.invitation).lower())
            ]
        except Exception:
            pass

    registered_signatures = set()
    for note in registration_notes:
        if hasattr(note, "signatures"):
            for sig in note.signatures:
                registered_signatures.add(sig.lower())

    rows = []
    for author in config.AUTHORS:
        or_id = author.get("openreview_id", "").lower()
        email = author.get("email", "").lower()
        matched = any(
            (or_id and or_id in sig) or (email and email in sig)
            for sig in registered_signatures
        )
        if matched:
            rows.append([author["name"], "Done", ""])
        elif not or_id and not email:
            rows.append([author["name"], "?", "No ID/email configured"])
        else:
            rows.append([author["name"], "PENDING", "Form not yet submitted"])

    headers = ["Author", "Status", "Note"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print(
        f"\nFound {len(registration_notes)} registration note(s) via API."
    )
    print(
        "Note: Registration visibility depends on API permissions.\n"
        "Use 'python openreview_agent.py browse' or ask each author to confirm directly.\n"
    )


def cmd_deadline(args):
    """Show time remaining until the registration deadline."""
    uk_tz = timezone(timedelta(hours=1))
    deadline = datetime(2026, 5, 28, 12, 0, 0, tzinfo=uk_tz)
    now = datetime.now(timezone.utc)
    remaining = deadline - now

    print("\n=== Registration Deadline ===\n")
    print(f"Deadline:  28 May 2026, 12:00 noon UK time (BST)")
    print(f"Now (UTC): {now.strftime('%Y-%m-%d %H:%M:%S')}")

    if remaining.total_seconds() > 0:
        days = remaining.days
        hours, rem = divmod(remaining.seconds, 3600)
        minutes = rem // 60
        print(f"Remaining: {days}d {hours}h {minutes}m")
        if days < 1:
            print("\n*** URGENT: Less than 24 hours remaining! ***")
    else:
        print("*** DEADLINE HAS PASSED ***")
    print()


def cmd_guide(args):
    """Print the recommended form-filling guide."""
    print("\n=== ARR Author Registration Form Guide ===\n")
    print(f"Form URL:\n  {config.FORM_URL}\n")
    print("--- Profile Checklist (do this first) ---")
    print("  [1] Full affiliation history with dates")
    print("  [2] All professional email addresses (current and past)")
    print("  [3] DBLP link (only if your page has no conflated papers)")
    print("  [4] Semantic Scholar link (same condition)")
    print("  [5] ACL Anthology link (if you have entries)")

    print("\n--- Recommended Form Answers ---\n")
    ra = config.RECOMMENDED_ANSWERS
    answers = [
        ["Willing to serve as reviewer/AC", ra["willing_to_serve"]],
        ["Qualified to review", ra["qualified_to_review"]],
        ["Emergency reviewer", ra["emergency_reviewer"]],
        ["Meta-data donation", ra["metadata_donation"]],
        ["Attribution", ra["attribution"]],
        ["Agreement", ra["agreement"]],
        ["Research areas (if serving)", ", ".join(ra["research_areas"])],
        ["Languages (if serving)", ", ".join(ra["languages"])],
    ]
    print(tabulate(answers, headers=["Question", "Recommended Answer"], tablefmt="grid"))

    print(
        "\nRationale: We rarely submit to ACL conferences, so none of us are likely\n"
        "to meet the reviewer bar (2+ papers in main ACL events + 1 in ACL Anthology\n"
        "or major AI venue). Select 'unqualified' — ARR will verify against DBLP.\n"
        "Do NOT write 'unqualified' in the justification field.\n"
    )


def cmd_browse(args):
    """Print instructions for Playwright MCP browser verification."""
    print("\n=== Playwright MCP Browser Verification ===\n")
    print("Use Claude Code with Playwright MCP to visually verify registration status.")
    print("Screenshots are saved to the screenshots/ directory.\n")
    print("Claude Code commands:\n")
    print('  claude -p "Log into OpenReview and screenshot the author tasks page. '
          'Save screenshots to screenshots/"')
    print()
    print('  claude -p "Navigate to the ARR author console and check which '
          'authors have completed the registration form"')
    print()
    print("Key URLs:")
    print(f"  Login:          https://openreview.net/login")
    print(f"  Author Console: https://openreview.net/group?id={config.VENUE_ID}/Authors")
    print(f"  Submission:     https://openreview.net/forum?id={config.SUBMISSION_ID}")
    print(f"  Form:           {config.FORM_URL}")
    print()


def cmd_status(args):
    """Full dashboard: deadline + profiles + submission + registration + guide."""
    args.client = get_client()
    cmd_deadline(args)
    cmd_profiles(args)
    cmd_submission(args)
    cmd_registration(args)
    cmd_guide(args)


def main():
    parser = argparse.ArgumentParser(
        description="OpenReview Registration Agent — ARR May 2026 / EMNLP 2026",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python openreview_agent.py status      # full dashboard\n"
            "  python openreview_agent.py profiles     # check author profiles\n"
            "  python openreview_agent.py submission   # check submission info\n"
            "  python openreview_agent.py guide        # form-filling guide\n"
            "  python openreview_agent.py deadline     # time until deadline\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Full dashboard (profiles + submission + registration + guide)")
    subparsers.add_parser("profiles", help="Check author OpenReview profiles")
    subparsers.add_parser("submission", help="Check submission details")
    subparsers.add_parser("registration", help="Check registration form status")
    subparsers.add_parser("guide", help="Print form-filling guide with recommended answers")
    subparsers.add_parser("deadline", help="Show time remaining until deadline")
    subparsers.add_parser("browse", help="Print Playwright MCP browser verification instructions")

    args = parser.parse_args()
    commands = {
        "status": cmd_status,
        "profiles": cmd_profiles,
        "submission": cmd_submission,
        "registration": cmd_registration,
        "guide": cmd_guide,
        "deadline": cmd_deadline,
        "browse": cmd_browse,
    }

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    commands[args.command](args)


if __name__ == "__main__":
    main()
