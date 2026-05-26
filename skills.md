# OpenReview Registration Agent — Skills

## Skill 1: Check Registration Status

**Trigger:** "check status", "who has registered", "registration status"

### Steps
1. Run `python openreview_agent.py status` for full dashboard
2. Or run individual commands: `profiles`, `submission`, `registration`, `deadline`, `guide`

### API Notes
- OpenReview rate-limits login to 3 requests per minute — use `status` (single session) instead of running multiple commands separately
- Registration notes may return 0 via API due to permission scoping — use Playwright for reliable visual verification

---

## Skill 2: Visual Verification via Playwright MCP

**Trigger:** "screenshot", "check visually", "verify on openreview", "log in and check"

### Steps
1. Navigate to `https://openreview.net/login`
2. Fill login form with credentials from `.credentials/.env`
3. Navigate to author console: `https://openreview.net/group?id=aclweb.org/ACL/ARR/2026/May/Authors`
4. Click "Author Tasks" tab to see registration task status
5. Take screenshots and save to `screenshots/`

### Key URLs
- Login: `https://openreview.net/login`
- Author Console: `https://openreview.net/group?id=aclweb.org/ACL/ARR/2026/May/Authors`
- Submission: `https://openreview.net/forum?id=Y7fud8ti4F`
- Registration Form Forum: `https://openreview.net/forum?id=eNnEx8x2CH`

---

## Skill 3: Fill & Submit Author Registration Form

**Trigger:** "fill out form", "submit registration", "register me"

### Prerequisites
- Must be logged into OpenReview via Playwright
- Credentials in `.credentials/.env`

### Steps
1. Navigate to author console and click "Author Tasks" tab
2. Click "Authors Submitted Author Form" link
3. Click "Submitted Author Form" button to open the form
4. Fill all required fields using click actions on radio buttons (not `fill_form` — radio `setChecked` can be unreliable):

| Field | Recommended Answer |
|---|---|
| Willing to serve as reviewer/AC | No, I cannot serve because I am unqualified |
| Details/justification | *(leave blank)* |
| Emergency reviewer | No, I am not willing to serve |
| Emergency load | N/A |
| Qualified to review | No, I do not meet the ARR requirements |
| Student | No, I am not a student |
| Education | Masters |
| Profile has past domains | Yes (checkbox) |
| Profile has all emails | Yes (checkbox) |
| Meta-data donation | Yes, I consent |
| Research areas | *(optional — skip if not serving)* |
| Languages | *(optional — skip if not serving)* |
| DBLP | No, I have no DBLP listed publications |
| DBLP URL | *(leave blank)* |
| Semantic Scholar | No, I have no Semantic Scholar listed publications |
| Semantic Scholar URL | *(leave blank)* |
| ACL Anthology URL | *(leave blank)* |
| Attribution | No, I do not wish to be attributed |
| Agreement | I agree (single cycle) |

5. Take screenshot of filled form before submitting
6. Click "Submit" button
7. Take screenshot of confirmation page showing "Submitted Author Form by [Name]"
8. Update `config.py` with the note ID from the confirmation

### Playwright Tips
- Use `browser_click` on radio buttons (more reliable than `browser_fill_form` with `type: "radio"`)
- Use `browser_fill_form` with `type: "checkbox"` for checkboxes (works correctly)
- Take `fullPage` screenshots at each stage: blank, filled, submitted
- Save all screenshots to `screenshots/` directory

---

## Skill 4: Check Deadline

**Trigger:** "how much time left", "deadline", "when is it due"

### Steps
1. Run `python openreview_agent.py deadline`
2. Deadline: 28 May 2026, 12:00 noon UK time (BST) = 29 May 2026, 14:59 EEST

---

## Skill 5: Generate Co-Author Instructions

**Trigger:** "send instructions to co-authors", "form guide", "what should they fill"

### Steps
1. Run `python openreview_agent.py guide`
2. Output includes profile checklist, recommended form answers, and rationale
3. Key message: authors who don't meet the reviewer bar (2+ papers in main ACL events) should select "unqualified" and leave the justification field blank

---

## Completed Registrations

| Author | Status | Date | Note ID |
|---|---|---|---|
| Julian Kaljuvee | Done | 26 May 2026 23:05 EEST | u21VQQHCQ1 |
| Chenhao Xue | PENDING | | |
| Raslen Guesmi | PENDING | | |
| Siwei Feng | PENDING | | |
| Yucheng Gong | PENDING | | |
| Jacob Xavier Sundram | PENDING | | |
| Jordan Pang | PENDING | | |
| Lan Wang | PENDING | | |
