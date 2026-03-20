#!/usr/bin/env python3
"""Populate the Ron Davis Primary Campaign Timeline Google Sheet."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_SHEETS
from googleapiclient.discovery import build

SHEET_ID = "1cON7YbzPDxoh4p1BydLKTpSRRXe3gL5BbZJo5WxB6n0"

HEADERS = ["Date", "Category", "Item", "Notes", "Status"]

ROWS = [
    ["5/4/2026", "Milestones & Key Dates", "Candidate Filing Window Opens (WA SOS)", "Declarations may be received by mail starting April 20, 2026. Must also submit to the Public Disclosure Commission within one business day after the filing period closes (by May 9, 2026).", "Not Started"],
    ["5/8/2026", "Milestones & Key Dates", "Candidate Filing Deadline (WA SOS)", "Source: sos.wa.gov/elections/calendar. Withdrawal deadline: May 11, 2026.", "Not Started"],
    ["Date TBC", "Milestones & Key Dates", "Campaign Launch", "Blue Streak owns", "Not Started"],
    ["5/11/2026", "Milestones & Key Dates", "Candidate Withdrawal Deadline", "Source: sos.wa.gov/elections/calendar", "Not Started"],
    ["6/1/2026", "Milestones & Key Dates", "Weekly PDC C-3 Reports Begin", "Filed every Monday through primary for prior week's deposits. Source: pdc.wa.gov/key-dates-2026", "Not Started"],
    ["7/14/2026", "Milestones & Key Dates", "PDC 21-Day Pre-Primary Report Due", "Covers Jun 1 – Jul 13, 2026. Source: pdc.wa.gov/key-dates-2026", "Not Started"],
    ["7/17/2026", "Milestones & Key Dates", "Ballots Mailed to Voters", "Based on 18-day rule. SOS calendar does not list this date explicitly — confirm with King County Auditor.", "Not Started"],
    ["7/27/2026", "Milestones & Key Dates", "Voter Registration Deadline (mail-in)", "", "Not Started"],
    ["7/28/2026", "Milestones & Key Dates", "PDC 7-Day Pre-Primary Report Due", "Covers Jul 14 – Jul 27, 2026. Last-minute contribution reports (≥$1,500 from single source) required Jul 28 – Aug 3. Source: pdc.wa.gov/key-dates-2026", "Not Started"],
]

def main():
    creds = get_credentials(SCOPES_SHEETS)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Rename the sheet tab and spreadsheet title
    sheet.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [
            {"updateSpreadsheetProperties": {
                "properties": {"title": "Ron Davis \u2014 Primary Campaign Timeline"},
                "fields": "title"
            }},
            {"updateSheetProperties": {
                "properties": {"sheetId": 0, "title": "Campaign Timeline"},
                "fields": "title"
            }}
        ]}
    ).execute()

    # Write headers and data
    values = [HEADERS] + ROWS
    sheet.values().update(
        spreadsheetId=SHEET_ID,
        range="Campaign Timeline!A1",
        valueInputOption="USER_ENTERED",
        body={"values": values}
    ).execute()

    # Format header row — bold, background color
    sheet.batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [
            # Bold headers
            {"repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True, "fontSize": 10,
                                   "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                    "backgroundColor": {"red": 0, "green": 0, "blue": 0},
                    "verticalAlignment": "MIDDLE"
                }},
                "fields": "userEnteredFormat(textFormat,backgroundColor,verticalAlignment)"
            }},
            # Body rows font
            {"repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 20},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"fontSize": 10},
                    "verticalAlignment": "TOP",
                    "wrapStrategy": "WRAP"
                }},
                "fields": "userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)"
            }},
            # Column widths
            {"updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 110}, "fields": "pixelSize"
            }},
            {"updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2},
                "properties": {"pixelSize": 160}, "fields": "pixelSize"
            }},
            {"updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3},
                "properties": {"pixelSize": 260}, "fields": "pixelSize"
            }},
            {"updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4},
                "properties": {"pixelSize": 340}, "fields": "pixelSize"
            }},
            {"updateDimensionProperties": {
                "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
                "properties": {"pixelSize": 110}, "fields": "pixelSize"
            }},
            # Freeze header row
            {"updateSheetProperties": {
                "properties": {"sheetId": 0, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount"
            }},
            # Format Date column as date
            {"repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 20,
                          "startColumnIndex": 0, "endColumnIndex": 1},
                "cell": {"userEnteredFormat": {
                    "numberFormat": {"type": "DATE", "pattern": "m/d/yyyy"}
                }},
                "fields": "userEnteredFormat.numberFormat"
            }},
            # Add filter to all columns
            {"setBasicFilter": {
                "filter": {
                    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 20,
                              "startColumnIndex": 0, "endColumnIndex": 5}
                }
            }}
        ]}
    ).execute()

    print(f"Done. Open here:\nhttps://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

if __name__ == "__main__":
    main()
