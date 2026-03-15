#!/usr/bin/env python3
"""Revert the Ron Davis SOW to plain text original."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

DOC_ID = "135Hn4vbX8DzU1fD_cAwtUxluKDJ90UnElo-xHqUGr4U"

ORIGINAL = """Friends of Ron Davis - SOW (proposed) V1

Proposed Statement of Work

Candidette Campaigns Consulting Services Proposal
This document is a proposal submitted for discussion and is not binding until signed by both parties. Terms are open to negotiation.

Parties

Consultant: Elizabeth Rosenberg dba Candidette Campaigns
Client: Friends of Ron Davis - Ron Davis, Candidate Washington State House of Representatives, Legislative District 46, Position 1

Engagement Overview

This Statement of Work outlines the scope, timeline, and compensation for limited campaign services to be provided by Candidette Campaigns to Friends of Ron Davis in support of the 2026 Washington State House campaign.

Term

This engagement begins March 16, 2026 and concludes June 8, 2026 (12 weeks), unless extended or terminated as provided below.

Scope of Services

Candidette Campaigns will provide consulting and project support in the following areas:

Campaign Operations

Create a campaign timeline, calculate vote goals, and create a preliminary field plan for early voter contact.
Manage the candidate's calendar to ensure campaign meetings, interviews, community and special events, and canvassing opportunities are scheduled.
Leverage Votebuilder or other campaign CRM for canvass script creation, volunteer and voter contact tracking, and related campaign functions.
Cover/manage staff email daily.

Volunteer Recruitment & Management

Create interim volunteer tracking document to support an eventual transition to Votebuilder or other campaign CRM.
Recruit volunteers to canvass.
Recruit \u201cspecial function\u201d volunteers: fundraising and special event set up, social media content creation, turf cutting, and website development.
Cut turf for field events, eventually with greater support from \u201cspecial function\u201d volunteers.
Create special event calendar to proactively identify public campaign opportunities (farmers markets, festivals, etc.) that may be leveraged by candidate and/or volunteers.
Create a simple canvass script for early voter outreach.
Support \u201ctraining the trainers\u201d by creating canvass training materials and checklists for super volunteers to leverage at launches.
Create a volunteer sign up system (Mobilize, Linktree, etc.) to advertise volunteer opportunities and make it easier for people to sign up to support the campaign.

Endorsement Support

Identify endorsement opportunities and create spreadsheet to track outreach, progress and results.
Assist candidate in endorsement outreach and schedule meetings as needed.

Compensation

Rate: $30.00 per hour
Hours: Approximately 10 hours per week for 12 weeks
Payment Schedule: Twice Monthly
Total Engagement Value: $3,600.00
Compensation is structured based on the hourly rate and expected weekly hours above.

Payment Terms

TO BE CONFIRMED
Payment Schedule: TBC
Payment method is flexible and will be determined by mutual agreement. Candidette Campaigns is open to check, ACH transfer, Zelle, or other arrangement convenient to the campaign.

Expenses

Out-of-pocket expenses incurred on behalf of the campaign (e.g., travel, printing, event supplies) are not included in the retainer and will be billed separately with prior approval from the Client. Receipts will be provided for all reimbursable expenses.

Termination

Either party may terminate this agreement with 14 days\u2019 written notice. In the event of termination, the Client shall compensate Candidette Campaigns for all hours worked through the termination date at the hourly rate specified above.

Confidentiality

Both parties agree to maintain confidentiality regarding campaign strategy, donor information, and any proprietary information shared during this engagement, consistent with the Mutual Confidentiality Agreement executed between the parties.

Acknowledgment

By signing below, both parties agree to the terms of this Statement of Work.

Consultant:
Signature: ___________________________________
Name: Elizabeth Rosenberg
Title: Principal, Elizabeth Rosenberg dba Candidette Campaigns
Date: ___________________________________

Client:
Signature: ___________________________________
Name: Ron Davis
Title: Candidate, Friends of Ron Davis
Date: ___________________________________
"""

def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 2) if content else 2

    requests = []
    if end_index > 2:
        requests.append({
            "deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": end_index - 1}
            }
        })

    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": ORIGINAL
        }
    })

    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests}
    ).execute()

    print("Reverted. Open here:")
    print(f"https://docs.google.com/document/d/{DOC_ID}/edit")

if __name__ == "__main__":
    main()
