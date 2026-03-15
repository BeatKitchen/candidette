#!/usr/bin/env python3
"""Read data from a Google Sheet.

Usage:
    python3 sheets_read.py SHEET_NAME_OR_ID [TAB_NAME]
    python3 sheets_read.py --test
    python3 sheets_read.py --list SHEET_NAME_OR_ID

Examples:
    python3 sheets_read.py sam_wang_tracker
    python3 sheets_read.py sam_wang_tracker "Budget"
    python3 sheets_read.py 1abc...xyz "Sheet1"
    python3 sheets_read.py --list sam_wang_tracker   # list all tabs
    python3 sheets_read.py --test                    # verify connection
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, resolve_sheet_id, SCOPES_SHEETS, CREDS_PATH

import gspread


def test_connection():
    """Verify credentials work."""
    creds = get_credentials(SCOPES_SHEETS)
    print(f"Connected successfully.")
    print(f"Service account: {creds.service_account_email}")


def list_tabs(sheet_id):
    """List all worksheet tabs in a spreadsheet."""
    creds = get_credentials(SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(sheet_id)
    for ws in spreadsheet.worksheets():
        print(f"  {ws.title} ({ws.row_count} rows x {ws.col_count} cols)")


def read_sheet(sheet_id, tab_name=None):
    """Read all data from a sheet tab. Returns list of dicts (header row = keys)."""
    creds = get_credentials(SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(sheet_id)

    if tab_name:
        worksheet = spreadsheet.worksheet(tab_name)
    else:
        worksheet = spreadsheet.sheet1

    records = worksheet.get_all_records()
    print(json.dumps(records, indent=2, default=str))
    return records


def main():
    parser = argparse.ArgumentParser(description="Read data from a Google Sheet")
    parser.add_argument("sheet", nargs="?", help="Sheet name (from registry) or ID")
    parser.add_argument("tab", nargs="?", help="Worksheet/tab name (default: first tab)")
    parser.add_argument("--test", action="store_true", help="Test connection only")
    parser.add_argument("--list", action="store_true", help="List all tabs in the sheet")
    args = parser.parse_args()

    if args.test:
        test_connection()
        return

    if not args.sheet:
        parser.print_help()
        sys.exit(1)

    sheet_id = resolve_sheet_id(args.sheet)

    if args.list:
        print(f"Tabs in {args.sheet}:")
        list_tabs(sheet_id)
    else:
        read_sheet(sheet_id, args.tab)


if __name__ == "__main__":
    main()
