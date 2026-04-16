#!/usr/bin/env python3
"""
Populate NJ-12 outreach contacts spreadsheet.

Sheet ID: 1m-zjEg5kO6mXxBpEVu85BR80sOPDEC8GuJHZxbI9Pn8

Columns:
  A: Contact Name
  B: Organization
  C: Type
  D: Links
  E: Email
  F: Phone

Types used:
  Party Organization
  Progressive Group
  AAPI Organization
  AI Policy Organization
  Reformers

Run from repo root:
  /tmp/candidette-venv/bin/python projects/sam-wang/notes/populate_contacts.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import gspread
from lib.google_auth import get_credentials, SCOPES_SHEETS

SHEET_ID = "1m-zjEg5kO6mXxBpEVu85BR80sOPDEC8GuJHZxbI9Pn8"

# Full contact list as of 2026-04-16
# Format: [Contact Name, Organization, Type, Links, Email, Phone]
CONTACTS = [
    # --- Party Organizations ---
    ["Julie Raskin", "Mercer County Democratic Committee", "Party Organization", "mercerdemocrats.org", "julie@mercerdemocrats.org", "609-571-5602"],
    ["Roger Kimball", "Middlesex County Democratic Organization", "Party Organization", "middlesexdemocrats.org", "rkimball@middlesexdemocrats.org", "732-246-1100"],
    ["Assemblyman Roy Freiman", "Somerset County Democratic Committee", "Party Organization", "somersetdems.org", "chair@somersetdems.org", "908-595-0949"],
    ["Carolyn Jacobson", "Hightstown Democratic Club", "Party Organization", "htowndemocrats.org", "", ""],
    ["Dave DeNapoli", "East Windsor Democratic Club", "Party Organization", "", "davedenapoli@gmail.com", ""],
    ["West Windsor Democratic Club", "West Windsor Democratic Club", "Party Organization", "wwdemclub.org", "info@wwdemclub.org", ""],
    ["Princeton Democratic Committee", "Princeton Democratic Committee", "Party Organization", "princetondems.org", "info@princetondems.org", ""],
    ["South Brunswick Democratic Club", "South Brunswick Democratic Club", "Party Organization", "", "", ""],
    ["Plainsboro Democratic Committee", "Plainsboro Democratic Committee", "Party Organization", "", "", ""],
    ["Cranbury Democratic Committee", "Cranbury Democratic Committee", "Party Organization", "", "", ""],
    ["Monroe Township Democratic Club", "Monroe Township Democratic Club", "Party Organization", "", "", ""],
    ["Jamesburg Democratic Club", "Jamesburg Democratic Club", "Party Organization", "", "", ""],
    ["Milltown Democratic Club", "Milltown Democratic Club", "Party Organization", "", "", ""],
    # --- Progressive Groups ---
    ["Sue Altman", "New Jersey Working Families Party", "Progressive Group", "njworkingfamilies.org", "suealtman@njworkingfamilies.org", "973-494-1716"],
    ["Sarah Fajardo", "ACLU of New Jersey", "Progressive Group", "aclu-nj.org", "sfajardo@aclu-nj.org", "973-642-2086"],
    ["Brandon McKoy", "New Jersey Policy Perspective", "Progressive Group", "njpp.org", "bmckoy@njpp.org", "609-393-1145"],
    ["Phyllis Salowe-Kaye", "New Jersey Citizen Action", "Progressive Group", "njcitizenaction.org", "psalowekaye@njcitizenaction.org", "973-643-8800"],
    ["Doug O'Malley", "Environment New Jersey", "Progressive Group", "environmentnewjersey.org", "domalley@environmentnewjersey.org", "609-403-3480"],
    ["Renée Steinhagen", "NJ Appleseed Public Interest Law Center", "Progressive Group", "njappleseed.org", "", "973-735-0523"],
    # --- AAPI Organizations ---
    ["Alfred Doblin", "Asian American Alliance of Mercer County", "AAPI Organization", "", "", ""],
    ["Ami Bera", "AAPI Victory Fund", "AAPI Organization", "aapivictoryfund.org", "info@aapivictoryfund.org", ""],
    ["Varun Nikore", "AAPI Victory Alliance", "AAPI Organization", "aapialliance.org", "varun@aapialliance.org", ""],
    ["Shekar Krishnan", "South Asian Americans Leading Together (SAALT)", "AAPI Organization", "saalt.org", "shekar@saalt.org", "301-270-1855"],
    ["Deepa Iyer", "South Asian Americans Leading Together (SAALT)", "AAPI Organization", "saalt.org", "deepa@saalt.org", "301-270-1855"],
    ["NJ Asian American Pacific Islander Affairs Commission", "NJ AAPI Affairs Commission", "AAPI Organization", "nj.gov/aapi", "", ""],
    # --- AI Policy Organizations ---
    ["Tithi Chattopadhyay", "Princeton Center for Information Technology Policy (CITP)", "AI Policy Organization", "citp.princeton.edu", "tithi@princeton.edu", "609-258-6167"],
    ["Liat Krawczyk", "NJ AI Hub (West Windsor)", "AI Policy Organization", "njaihub.org", "", ""],
    # --- Reformers ---
    ["Herb Tarbous", "Voter Choice NJ", "Reformers", "voterchoicenj.org", "", ""],
    ["Renée Steinhagen", "NJ Appleseed Public Interest Law Center", "Reformers", "njappleseed.org", "", "973-735-0523"],
    ["Meredith Sumpter", "FairVote", "Reformers", "fairvote.org", "info@fairvote.org", "(301) 270-4616"],
    ["Josh Orton", "Demand Justice", "Reformers", "demandjustice.org", "press@demandjustice.org", ""],
    ["Sarah Lipton-Lubet", "Take Back the Court Action Fund", "Reformers", "takebackthecourt.today", "", ""],
    ["John Koza", "National Popular Vote Inc.", "Reformers", "nationalpopularvote.com", "", ""],
]


def main():
    creds = get_credentials(SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.get_worksheet(0)

    # Clear existing data below header and rewrite
    ws.clear()

    header = ["Contact Name", "Organization", "Type", "Links", "Email", "Phone"]
    all_rows = [header] + CONTACTS

    ws.update("A1", all_rows, value_input_option="USER_ENTERED")
    print(f"Written {len(CONTACTS)} contacts + header.")

    # Format header: bold, light blue fill, center align, freeze row 1
    last_row = len(all_rows)
    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": ws.id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 6,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.68, "green": 0.85, "blue": 0.9},
                        "horizontalAlignment": "CENTER",
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)",
            }
        },
        {
            "updateSheetProperties": {
                "properties": {"sheetId": ws.id, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount",
            }
        },
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": ws.id,
                        "startRowIndex": 0,
                        "endRowIndex": last_row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 6,
                    }
                }
            }
        },
    ]
    sh.batch_update({"requests": requests})
    print("Header formatted, row frozen, filter applied.")


if __name__ == "__main__":
    main()
