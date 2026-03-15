#!/usr/bin/env python3
"""Write data to a Google Sheet.

Usage:
    python3 sheets_write.py SHEET TAB --append ROW_JSON
    python3 sheets_write.py SHEET TAB --update CELL VALUE
    python3 sheets_write.py SHEET TAB --batch-update UPDATES_JSON

Examples:
    # Append a row
    python3 sheets_write.py sam_wang_tracker "Tasks" --append '["Call donors", "2026-03-20", "Liz", "pending"]'

    # Update a single cell
    python3 sheets_write.py sam_wang_tracker "Budget" --update B5 "5000"

    # Batch update multiple cells
    python3 sheets_write.py sam_wang_tracker "Budget" --batch-update '[{"cell": "B5", "value": "5000"}, {"cell": "B6", "value": "3200"}]'
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, resolve_sheet_id, SCOPES_SHEETS

import gspread


def append_row(sheet_id, tab_name, row_data):
    """Append a row to the bottom of a sheet."""
    creds = get_credentials(SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(tab_name)

    worksheet.append_row(row_data, value_input_option="USER_ENTERED")
    print(f"Appended row to '{tab_name}': {row_data}")


def update_cell(sheet_id, tab_name, cell, value):
    """Update a single cell."""
    creds = get_credentials(SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(tab_name)

    worksheet.update_acell(cell, value)
    print(f"Updated {cell} in '{tab_name}' to: {value}")


def batch_update(sheet_id, tab_name, updates):
    """Update multiple cells. updates = [{"cell": "A1", "value": "foo"}, ...]"""
    creds = get_credentials(SCOPES_SHEETS)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(tab_name)

    for u in updates:
        worksheet.update_acell(u["cell"], u["value"])
        print(f"Updated {u['cell']} in '{tab_name}' to: {u['value']}")

    print(f"Batch update complete: {len(updates)} cells updated.")


def main():
    parser = argparse.ArgumentParser(description="Write data to a Google Sheet")
    parser.add_argument("sheet", help="Sheet name (from registry) or ID")
    parser.add_argument("tab", help="Worksheet/tab name")
    parser.add_argument("--append", help="JSON array of values to append as a row")
    parser.add_argument("--update", nargs=2, metavar=("CELL", "VALUE"), help="Update a single cell")
    parser.add_argument("--batch-update", help="JSON array of {cell, value} objects")
    args = parser.parse_args()

    sheet_id = resolve_sheet_id(args.sheet)

    if args.append:
        row_data = json.loads(args.append)
        append_row(sheet_id, args.tab, row_data)
    elif args.update:
        cell, value = args.update
        update_cell(sheet_id, args.tab, cell, value)
    elif args.batch_update:
        updates = json.loads(args.batch_update)
        batch_update(sheet_id, args.tab, updates)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
