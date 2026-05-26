# OpenReview Registration Agent

Manages and monitors author registration status for the ARR May 2026 / EMNLP 2026 submission on OpenReview.

**Paper:** Temporal Leakage in Financial News NLP: A Multi-Architecture Audit with a Regime-Specific M&A Signal
**Submission:** [Y7fud8ti4F](https://openreview.net/forum?id=Y7fud8ti4F) | **Form forum:** [eNnEx8x2CH](https://openreview.net/forum?id=eNnEx8x2CH)
**Deadline:** 28 May 2026, 12:00 noon UK time (BST)

## Authors

| Author | Affiliation | OpenReview ID |
|---|---|---|
| Chenhao Xue | University of Oxford | `~Chenhao_Xue2` |
| Raslen Guesmi | University of Carthage | `~Raslen_Guesmi2` |
| Siwei Feng | Predictive Labs / University of Oxford | `~Siwei_Feng3` |
| Yucheng Gong | Imperial College London | `~Yucheng_Gong4` |
| Jacob Xavier Sundram | Imperial College London | `~Jacob_Xavier_Sundram1` |
| Jordan Pang | Imperial College London | `~Jordan_Pang1` |
| Lan Wang | Independent Researcher / University of Oxford | `~Lan_Wang13` |
| Julian Kaljuvee | Harvard University / Columbia University | `~Julian_Kaljuvee1` |

## Setup

```bash
# Install dependencies
uv pip install -r requirements.txt

# Configure credentials
cp .credentials/.env.example .credentials/.env
# Edit .credentials/.env with your OpenReview username and password
```

Add co-author emails in `config.py` to enable profile lookups and registration tracking.

## Usage

### Python CLI

```bash
# Full dashboard — deadline, profiles, submission, registration status, guide
python openreview_agent.py status

# Check author OpenReview profiles
python openreview_agent.py profiles

# Check submission details
python openreview_agent.py submission

# Check registration form completion
python openreview_agent.py registration

# Print form-filling guide with recommended answers
python openreview_agent.py guide

# Show time remaining until deadline
python openreview_agent.py deadline

# Print Playwright browser verification instructions
python openreview_agent.py browse
```

### Claude Code

```bash
# Check overall status
claude -p "Run python openreview_agent.py status and summarize the results"

# Check who still needs to register
claude -p "Run python openreview_agent.py registration and tell me who hasn't completed the form yet"

# Quick deadline check
claude -p "Run python openreview_agent.py deadline"

# Get the form-filling guide
claude -p "Run python openreview_agent.py guide and format it as a message I can send to co-authors"
```

### Playwright MCP (Visual Verification)

Use Claude Code with the Playwright MCP plugin to log into OpenReview and visually verify registration status. Screenshots are saved to `screenshots/`.

```bash
# Log in and screenshot the author tasks page
claude -p "Use Playwright to log into OpenReview and screenshot the author console. Save to screenshots/"

# Check registration form visually
claude -p "Navigate to the ARR author console and check which authors have completed the registration form. Take screenshots."
```

## Configuration

### Credentials (`.credentials/.env`)

```
OPENREVIEW_USERNAME=your_openreview_email@example.com
OPENREVIEW_PASSWORD=your_openreview_password
```

The `.credentials/` directory is gitignored. Never commit credentials.

### Authors (`config.py`)

Authors include OpenReview profile IDs for reliable lookups:

```python
AUTHORS = [
    {"name": "Chenhao Xue", "email": "", "openreview_id": "~Chenhao_Xue2"},
    {"name": "Raslen Guesmi", "email": "", "openreview_id": "~Raslen_Guesmi2"},
    {"name": "Siwei Feng", "email": "", "openreview_id": "~Siwei_Feng3"},
    {"name": "Yucheng Gong", "email": "", "openreview_id": "~Yucheng_Gong4"},
    {"name": "Jacob Xavier Sundram", "email": "", "openreview_id": "~Jacob_Xavier_Sundram1"},
    {"name": "Jordan Pang", "email": "", "openreview_id": "~Jordan_Pang1"},
    {"name": "Lan Wang", "email": "", "openreview_id": "~Lan_Wang13"},
    {"name": "Julian Kaljuvee", "email": "kaljuvee@gmail.com", "openreview_id": "~Julian_Kaljuvee1"},
]
```

## Architecture

| File | Purpose |
|---|---|
| `openreview_agent.py` | CLI entry point — profile checks, submission lookup, registration status, guide |
| `config.py` | Paper metadata, author list, venue IDs, recommended form answers |
| `browse.py` | Documents the Playwright MCP browser workflow for visual verification |
| `screenshots/` | Playwright-captured screenshots (contents gitignored, `.gitkeep` tracked) |
| `.credentials/.env` | OpenReview login credentials (gitignored) |
| `requirements.txt` | Python dependencies |
