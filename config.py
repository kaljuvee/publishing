"""Configuration for ARR May 2026 submission and author registration tracking."""

VENUE_ID = "aclweb.org/ACL/ARR/2026/May"
FORUM_ID = "eNnEx8x2CH"
SUBMISSION_ID = "Y7fud8ti4F"
NOTE_ID = "wtEpVpRryA"
SUBMISSION_DEADLINE = "2026-05-28T12:00:00+01:00"

PAPER_TITLE = (
    "Temporal Leakage in Financial News NLP: "
    "A Multi-Architecture Audit with a Regime-Specific M&A Signal"
)

AUTHORS = [
    {"name": "Chenhao Xue", "email": "", "openreview_id": "~Chenhao_Xue2"},
    {"name": "Raslen Guesmi", "email": "", "openreview_id": "~Raslen_Guesmi2"},
    {"name": "Siwei Feng", "email": "", "openreview_id": "~Siwei_Feng3"},
    {"name": "Yucheng Gong", "email": "", "openreview_id": "~Yucheng_Gong4"},
    {"name": "Jacob Xavier Sundram", "email": "", "openreview_id": "~Jacob_Xavier_Sundram1"},
    {"name": "Jordan Pang", "email": "", "openreview_id": "~Jordan_Pang1"},
    {"name": "Lan Wang", "email": "", "openreview_id": "~Lan_Wang13"},
    {"name": "Julian Kaljuvee", "email": "kaljuvee@post.harvard.edu", "openreview_id": "~Julian_Kaljuvee1"},
]

FORM_URL = (
    "https://openreview.net/forum?id=eNnEx8x2CH"
    "&noteId=wtEpVpRryA"
    "&referrer=%5BAuthor%20Console%5D"
    "(%2Fgroup%3Fid%3Daclweb.org%2FACL%2FARR%2F2026%2FMay%2FAuthors%23author-tasks)"
)

SUBMISSION_URL = (
    "https://openreview.net/group?id=aclweb.org/ACL/ARR/2026/May/Authors#your-submissions"
)

RECOMMENDED_ANSWERS = {
    "willing_to_serve": (
        "No, I cannot serve because I am unqualified "
        "(we will check this and if you are qualified you will be required to review)."
    ),
    "qualified_to_review": "No, I do not meet the ARR requirements to be a reviewer.",
    "emergency_reviewer": "No, I am not willing to serve as an emergency reviewer or AC.",
    "emergency_load": "N/A, in the previous question I indicated I do not wish to be an emergency reviewer or AC.",
    "student": "No, I am not a student.",
    "education": "Masters",
    "profile_past_domains": "Yes",
    "profile_all_emails": "Yes",
    "metadata_donation": "Yes, I consent to donating anonymous metadata of my review for research.",
    "dblp": "No, I have no DBLP listed publications.",
    "semantic_scholar": "No, I have no Semantic Scholar listed publications.",
    "attribution": "No, I do not wish to be attributed.",
    "agreement": "I agree",
    "research_areas": [
        "NLP Applications",
        "Efficient Methods for NLP",
        "Machine Learning for NLP",
    ],
    "languages": ["English"],
}

# Julian Kaljuvee's form submitted 26 May 2026 23:05 EEST, note ID: u21VQQHCQ1
JULIAN_REGISTRATION_NOTE_ID = "u21VQQHCQ1"
