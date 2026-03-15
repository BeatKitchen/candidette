#!/usr/bin/env python3
"""Create a formatted version of the Ron Davis SOW."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

TITLE = "Friends of Ron Davis – Proposed Statement of Work"

FONT = "Arial"
BODY_SIZE = 10
H1_SIZE = 9
H2_SIZE = 10

SECTIONS = [
    ("Proposed Statement of Work", "title"),
    ("Candidette Campaigns  |  Consulting Services Proposal", "subtitle"),
    ("This document is a proposal submitted for discussion and is not binding until signed by both parties. Terms are open to negotiation.", "italic"),
    ("Parties", "heading1"),
    ("Consultant:  Elizabeth Rosenberg dba Candidette Campaigns", "body"),
    ("Client:  Friends of Ron Davis \u2013 Ron Davis, Candidate\nWashington State House of Representatives, Legislative District 46, Position 1", "body"),
    ("Engagement Overview", "heading1"),
    ("This Statement of Work outlines the scope, timeline, and compensation for limited campaign services to be provided by Candidette Campaigns to Friends of Ron Davis in support of the 2026 Washington State House campaign.", "body"),
    ("Term", "heading1"),
    ("This engagement begins March 16, 2026 and concludes June 8, 2026 (12 weeks), unless extended or terminated as provided below.", "body"),
    ("Scope of Services", "heading1"),
    ("Candidette Campaigns will provide consulting and project support in the following areas:", "body"),
    ("Campaign Operations", "heading2"),
    ("Create a campaign timeline, calculate vote goals, and create a preliminary field plan for early voter contact.", "bullet"),
    ("Manage the candidate\u2019s calendar to ensure campaign meetings, interviews, community and special events, and canvassing opportunities are scheduled.", "bullet"),
    ("Leverage Votebuilder or other campaign CRM for canvass script creation, volunteer and voter contact tracking, and related campaign functions.", "bullet"),
    ("Cover/manage staff email daily.", "bullet"),
    ("Volunteer Recruitment & Management", "heading2"),
    ("Create interim volunteer tracking document to support an eventual transition to Votebuilder or other campaign CRM.", "bullet"),
    ("Recruit volunteers to canvass.", "bullet"),
    ("Recruit \u201cspecial function\u201d volunteers: fundraising and special event set up, social media content creation, turf cutting, and website development.", "bullet"),
    ("Cut turf for field events, eventually with greater support from \u201cspecial function\u201d volunteers.", "bullet"),
    ("Create special event calendar to proactively identify public campaign opportunities (farmers markets, festivals, etc.) that may be leveraged by candidate and/or volunteers.", "bullet"),
    ("Create a simple canvass script for early voter outreach.", "bullet"),
    ("Support \u201ctraining the trainers\u201d by creating canvass training materials and checklists for super volunteers to leverage at launches.", "bullet"),
    ("Create a volunteer sign up system (Mobilize, Linktree, etc.) to advertise volunteer opportunities and make it easier for people to sign up to support the campaign.", "bullet"),
    ("Endorsement Support", "heading2"),
    ("Identify endorsement opportunities and create spreadsheet to track outreach, progress and results.", "bullet"),
    ("Assist candidate in endorsement outreach and schedule meetings as needed.", "bullet"),
    ("Compensation", "heading1"),
    ("Rate:  $30.00 per hour\nHours:  Approximately 10 hours per week for 12 weeks\nPayment Schedule:  Twice Monthly\nTotal Engagement Value:  $3,600.00", "body"),
    ("Compensation is structured based on the hourly rate and expected weekly hours above.", "body"),
    ("Payment Terms", "heading1"),
    ("TO BE CONFIRMED", "bold_body"),
    ("Payment Schedule:  TBC", "body"),
    ("Payment method is flexible and will be determined by mutual agreement. Candidette Campaigns is open to check, ACH transfer, Zelle, or other arrangement convenient to the campaign.", "body"),
    ("Expenses", "heading1"),
    ("Out-of-pocket expenses incurred on behalf of the campaign (e.g., travel, printing, event supplies) are not included in the retainer and will be billed separately with prior approval from the Client. Receipts will be provided for all reimbursable expenses.", "body"),
    ("Termination", "heading1"),
    ("Either party may terminate this agreement with 14 days\u2019 written notice. In the event of termination, the Client shall compensate Candidette Campaigns for all hours worked through the termination date at the hourly rate specified above.", "body"),
    ("Confidentiality", "heading1"),
    ("Both parties agree to maintain confidentiality regarding campaign strategy, donor information, and any proprietary information shared during this engagement, consistent with the Mutual Confidentiality Agreement executed between the parties.", "body"),
    ("Acknowledgment", "heading1"),
    ("By signing below, both parties agree to the terms of this Statement of Work.", "body"),
    ("Consultant", "heading2"),
    ("Signature: ___________________________________________________", "sig"),
    ("Name:  Elizabeth Rosenberg", "sig"),
    ("Title:  Principal, Elizabeth Rosenberg dba Candidette Campaigns", "sig"),
    ("Date:  ___________________________________________________", "sig"),
    ("Client", "heading2"),
    ("Signature: ___________________________________________________", "sig"),
    ("Name:  Ron Davis", "sig"),
    ("Title:  Candidate, Friends of Ron Davis", "sig"),
    ("Date:  ___________________________________________________", "sig"),
]

def txt(style_requests, index, length, font, size, bold=False, italic=False, color=None):
    ts = {"weightedFontFamily": {"fontFamily": font}, "fontSize": {"magnitude": size, "unit": "PT"}}
    fields = "weightedFontFamily,fontSize"
    if bold:
        ts["bold"] = True
        fields += ",bold"
    if italic:
        ts["italic"] = True
        fields += ",italic"
    if color:
        ts["foregroundColor"] = {"color": {"rgbColor": color}}
        fields += ",foregroundColor"
    style_requests.append({"updateTextStyle": {
        "range": {"startIndex": index, "endIndex": index + length - 1},
        "textStyle": ts,
        "fields": fields
    }})

def build_requests(sections):
    requests = []
    index = 1

    for text, style in sections:
        content = text + "\n"
        length = len(content)

        requests.append({"insertText": {"location": {"index": index}, "text": content}})

        if style == "title":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 18, bold=False)

        elif style == "subtitle":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 10, color={"red": 0.4, "green": 0.4, "blue": 0.4})

        elif style == "italic":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 20, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 9, italic=True,
                color={"red": 0.4, "green": 0.4, "blue": 0.4})

        elif style == "heading1":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 20, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                    "borderBottom": {
                        "color": {"color": {"rgbColor": {"red": 0.0, "green": 0.0, "blue": 0.0}}},
                        "width": {"magnitude": 0.5, "unit": "PT"},
                        "padding": {"magnitude": 2, "unit": "PT"},
                        "dashStyle": "SOLID"
                    }
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,borderBottom"
            }})
            txt(requests, index, length, FONT, H1_SIZE, bold=True)

        elif style == "heading2":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 12, "unit": "PT"},
                    "spaceBelow": {"magnitude": 3, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, H2_SIZE, bold=True,
                color={"red": 0.3, "green": 0.3, "blue": 0.3})

        elif style == "bullet":
            requests.append({"createParagraphBullets": {
                "range": {"startIndex": index, "endIndex": index + length},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
            }})
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "spaceAbove": {"magnitude": 1, "unit": "PT"},
                    "spaceBelow": {"magnitude": 1, "unit": "PT"},
                },
                "fields": "spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, BODY_SIZE)

        elif style == "bold_body":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, BODY_SIZE, bold=True)

        elif style == "sig":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 8, "unit": "PT"},
                    "spaceBelow": {"magnitude": 0, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, BODY_SIZE)

        else:  # body
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, BODY_SIZE)

        index += length

    return requests


DOC_ID = "135Hn4vbX8DzU1fD_cAwtUxluKDJ90UnElo-xHqUGr4U"

def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

    # Get current doc length so we can clear it
    doc = service.documents().get(documentId=DOC_ID).execute()
    body = doc.get("body", {})
    content = body.get("content", [])
    end_index = content[-1].get("endIndex", 2) if content else 2

    # Clear existing content (leave index 1, delete everything else)
    clear_requests = []
    if end_index > 2:
        clear_requests.append({
            "deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": end_index - 1}
            }
        })
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": clear_requests}
        ).execute()

    # Insert formatted content
    requests = build_requests(SECTIONS)
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests}
    ).execute()

    url = f"https://docs.google.com/document/d/{DOC_ID}/edit"
    print(f"Done. Open here:\n{url}")


if __name__ == "__main__":
    main()
