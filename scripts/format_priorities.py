#!/usr/bin/env python3
"""Write and format the Ron Davis campaign priorities into a shared Google Doc."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

DOC_ID = "1zLB_YZtZENNoiX9XrQvHaaQejCyAIQJUMl1KL0vh7Gk"
FONT = "Arial"

SECTIONS = [
    ("Friends of Ron Davis — March–June 2026 Campaign Priorities", "title"),

    ("Phase 1: Foundation  (March 16–31)", "heading1"),
    ("Goal: Get the infrastructure in place before activation begins.", "goal"),

    ("Campaign Operations", "heading2"),
    ("Create campaign timeline and calculate vote goals.", "bullet"),
    ("Begin managing candidate calendar.", "bullet"),
    ("Set up staff email coverage.", "bullet"),
    ("Create preliminary field plan: identify priority precincts.", "bullet"),

    ("Volunteer Recruitment & Management", "heading2"),
    ("Create interim volunteer tracking document.", "bullet"),
    ("Create volunteer sign-up system (Mobilize, Linktree, etc.).", "bullet"),
    ("Create special event calendar — identify public opportunities April–June.", "bullet"),

    ("Endorsement Support", "heading2"),
    ("Create endorsement tracking spreadsheet.", "bullet"),
    ("Begin identifying endorsement opportunities with candidate.", "bullet"),

    ("Phase 2: Building  (April)", "heading1"),
    ("Goal: Recruit the team, develop materials, begin outreach.", "goal"),

    ("Campaign Operations", "heading2"),
    ("Leverage Votebuilder/CRM for voter contact and script tracking.", "bullet"),
    ("Continue calendar management and email coverage.", "bullet"),

    ("Volunteer Recruitment & Management", "heading2"),
    ("Begin recruiting general canvass volunteers.", "bullet"),
    ("Begin recruiting \u201cspecial function\u201d volunteers (social media, turf cutting, events, website).", "bullet"),
    ("Create simple canvass script for early voter outreach.", "bullet"),

    ("Endorsement Support", "heading2"),
    ("Begin endorsement outreach with candidate.", "bullet"),
    ("Schedule endorsement meetings as needed.", "bullet"),

    ("Phase 3: Activation  (May)", "heading1"),
    ("Goal: Get volunteers in the field. Candidate visible in the community.", "goal"),

    ("Campaign Operations", "heading2"),
    ("Continue calendar management, email coverage, and CRM tracking.", "bullet"),

    ("Volunteer Recruitment & Management", "heading2"),
    ("Create canvass training materials and checklists for super-volunteers.", "bullet"),
    ("Support \u201ctrain the trainers\u201d \u2014 prep super-volunteers to lead canvass launches.", "bullet"),
    ("Increase turf cutting with greater support from special function volunteers.", "bullet"),

    ("Endorsement Support", "heading2"),
    ("Continue endorsement outreach and tracking.", "bullet"),

    ("Phase 4: Handoff & Wrap  (June 1–8)", "heading1"),
    ("Goal: Leave the campaign set up to continue without a gap.", "goal"),

    ("Transition volunteer tracking to Votebuilder or CRM.", "bullet"),
    ("Brief super-volunteers on ongoing responsibilities.", "bullet"),
    ("Deliver final materials, checklists, and calendar.", "bullet"),
    ("Wrap endorsement tracker and note outstanding outreach.", "bullet"),
]

def txt(requests, index, length, font, size, bold=False, italic=False, color=None):
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
    requests.append({"updateTextStyle": {
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
                    "alignment": "START",
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 18)

        elif style == "subtitle":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 20, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 10,
                color={"red": 0.4, "green": 0.4, "blue": 0.4})

        elif style == "heading1":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 22, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                    "borderBottom": {
                        "color": {"color": {"rgbColor": {"red": 0.0, "green": 0.0, "blue": 0.0}}},
                        "width": {"magnitude": 0.5, "unit": "PT"},
                        "padding": {"magnitude": 2, "unit": "PT"},
                        "dashStyle": "SOLID"
                    }
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,borderBottom"
            }})
            txt(requests, index, length, FONT, 12, bold=True)

        elif style == "goal":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 10, italic=True,
                color={"red": 0.4, "green": 0.4, "blue": 0.4})

        elif style == "heading2":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 10, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 11, bold=True)

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
            txt(requests, index, length, FONT, 11)

        index += length

    return requests


def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

    # Clear existing content
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 2) if content else 2

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

    # Write formatted content
    requests = build_requests(SECTIONS)
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests}
    ).execute()

    print(f"Done. Open here:\nhttps://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
