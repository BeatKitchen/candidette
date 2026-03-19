#!/usr/bin/env python3
"""Generate a monthly invoice for Ron Davis from the Hours Tracker.

Usage:
    python3 invoice_generate.py               # bills all unbilled hours
    python3 invoice_generate.py --month 2026-03  # bills unbilled hours for March 2026 only
    python3 invoice_generate.py --dry-run        # preview without creating doc or marking rows

What it does:
    1. Reads unbilled rows from the Hours Log tab
    2. Calculates total hours and amount
    3. Creates a new Google Doc invoice in the Ron Davis Drive folder
    4. Marks billed rows as "Billed" with the invoice number
    5. Increments the invoice counter in Settings
"""

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS, SCOPES_DRIVE

SCOPES = SCOPES_DOCS + SCOPES_DRIVE + ["https://www.googleapis.com/auth/spreadsheets"]

TRACKER_ID  = "1D8A7tVId1yJUlkE77dUpXIql5S2ryU-mg61hFBwhpu0"
FOLDER_ID   = "1FiCGD3KG5zRtO_P_RJc90hZDsK_g1z_p"
RATE        = 30.00

# Liz's details
LIZ_NAME    = "Elizabeth Rosenberg"
LIZ_DBA     = "d/b/a Candidette Campaigns"
LIZ_ADDRESS = "734 16th Avenue East, Seattle, WA 98112"
LIZ_PHONE   = "973-865-9031"
LIZ_EMAIL   = "Liz@candidette.com"
TRACKER_URL = f"https://docs.google.com/spreadsheets/d/{TRACKER_ID}/edit"


def get_nth_friday(year, month, n):
    """Return the nth Friday of the given month (n=1 for first, n=3 for third)."""
    first = date(year, month, 1)
    # weekday(): Monday=0 ... Friday=4
    days_until_friday = (4 - first.weekday()) % 7
    first_friday = first + timedelta(days=days_until_friday)
    return first_friday + timedelta(weeks=n - 1)


def payment_due_dates(invoice_date):
    """Return the 1st and 3rd Fridays of the month following invoice_date."""
    year  = invoice_date.year
    month = invoice_date.month + 1
    if month > 12:
        month = 1
        year += 1
    fri1 = get_nth_friday(year, month, 1)
    fri3 = get_nth_friday(year, month, 3)
    return fri1, fri3


def read_unbilled_rows(service, month_filter=None):
    """Read unbilled rows from Hours Log. Returns list of (row_index, row_data)."""
    result = service.spreadsheets().values().get(
        spreadsheetId=TRACKER_ID,
        range="Hours Log!A2:G500",
        valueRenderOption="FORMATTED_VALUE"
    ).execute()
    rows = result.get("values", [])

    unbilled = []
    for i, row in enumerate(rows, start=2):  # 1-indexed; row 1 is header
        if len(row) < 6:
            continue
        date_str = row[0].strip()
        status   = row[5].strip() if len(row) > 5 else ""
        hours    = row[3].strip() if len(row) > 3 else ""
        if not date_str or not hours or status != "Unbilled":
            continue
        if month_filter:
            # month_filter = "2026-03"
            try:
                from datetime import datetime
                d = datetime.strptime(date_str, "%b %d, %Y")
                if d.strftime("%Y-%m") != month_filter:
                    continue
            except ValueError:
                pass
        unbilled.append((i, row))
    return unbilled


def get_next_invoice_number(service):
    result = service.spreadsheets().values().get(
        spreadsheetId=TRACKER_ID,
        range="Settings!B2"
    ).execute()
    last = int(result["values"][0][0])
    return last + 1


def save_invoice_number(service, n):
    service.spreadsheets().values().update(
        spreadsheetId=TRACKER_ID,
        range="Settings!B2",
        valueInputOption="RAW",
        body={"values": [[n]]}
    ).execute()


def mark_rows_billed(service, row_indices, invoice_num):
    from googleapiclient.discovery import build
    for idx in row_indices:
        service.spreadsheets().values().update(
            spreadsheetId=TRACKER_ID,
            range=f"Hours Log!F{idx}:G{idx}",
            valueInputOption="USER_ENTERED",
            body={"values": [["Billed", invoice_num]]}
        ).execute()


def create_invoice_doc(docs_service, drive_service, invoice_num, invoice_date,
                       billing_period, rows, total_hours, total_amount):
    """Create the invoice Google Doc and return its URL."""
    fri1, fri3 = payment_due_dates(invoice_date)
    invoice_label = f"INV-DAVIS-{invoice_num:03d}"
    title = f"Candidette Campaigns — Invoice {invoice_label}"

    # Build plain text content
    lines = [
        f"{LIZ_NAME}",
        f"{LIZ_DBA}",
        f"{LIZ_ADDRESS}",
        f"{LIZ_PHONE}  |  {LIZ_EMAIL}",
        "",
        "INVOICE",
        "",
        f"Invoice #:        {invoice_label}",
        f"Invoice Date:     {invoice_date.strftime('%B %d, %Y')}",
        f"Billing Period:   {billing_period}",
        "",
        "BILL TO:",
        "Friends of Ron Davis",
        "Ron Davis for WA State House — LD46, Position 1",
        "",
        "SERVICES RENDERED:",
        "",
    ]

    # Line items
    col_widths = (14, 8, 8, 7)
    header_line = f"{'Date':<{col_widths[0]}}{'Start':<{col_widths[1]}}{'End':<{col_widths[2]}}{'Hrs':>{col_widths[3]}}    Description"
    lines.append(header_line)
    lines.append("-" * 90)

    for _, row in rows:
        date_str  = row[0] if len(row) > 0 else ""
        start_str = row[1] if len(row) > 1 else ""
        end_str   = row[2] if len(row) > 2 else ""
        hrs_str   = row[3] if len(row) > 3 else ""
        desc_str  = row[4] if len(row) > 4 else ""
        lines.append(
            f"{date_str:<{col_widths[0]}}"
            f"{start_str:<{col_widths[1]}}{end_str:<{col_widths[2]}}"
            f"{hrs_str:>{col_widths[3]}}    {desc_str}"
        )

    lines += [
        "-" * 90,
        f"{'TOTAL HOURS:':<{sum(col_widths)}}    {total_hours:.2f}",
        "",
        f"Rate:             ${RATE:.2f}/hour",
        f"TOTAL DUE:        ${total_amount:,.2f}",
        "",
        "─" * 90,
        "PAYMENT INSTRUCTIONS",
        "─" * 90,
        "",
        f"Please remit payment via Zelle to {LIZ_PHONE}.",
        "",
        "The total amount due may be paid in two equal installments:",
        f"  • First payment  ({fri1.strftime('%B %d, %Y')}):   ${total_amount/2:,.2f}",
        f"  • Second payment ({fri3.strftime('%B %d, %Y')}):   ${total_amount/2:,.2f}",
        "",
        "─" * 90,
        "TIME TRACKING REFERENCE",
        "─" * 90,
        "",
        f"Full hours log: {TRACKER_URL}",
        "",
    ]

    content = "\n".join(lines)

    # Create doc via Drive API (avoids service account quota issue)
    file_metadata = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [FOLDER_ID]
    }
    f = drive_service.files().create(body=file_metadata, fields="id, name").execute()
    doc_id = f["id"]

    # Insert content
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}
    ).execute()

    # Bold key lines
    doc = docs_service.documents().get(documentId=doc_id).execute()
    bold_targets = ["INVOICE", "BILL TO:", "SERVICES RENDERED:",
                    "TOTAL DUE:", "PAYMENT INSTRUCTIONS", "TIME TRACKING REFERENCE",
                    invoice_label, "TOTAL HOURS:"]
    bold_requests = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        text = "".join(r.get("textRun", {}).get("content", "") for r in elem["paragraph"].get("elements", []))
        for target in bold_targets:
            if target in text:
                si = elem["startIndex"]
                ei = elem["endIndex"] - 1
                bold_requests.append({"updateTextStyle": {
                    "range": {"startIndex": si, "endIndex": ei},
                    "textStyle": {"bold": True},
                    "fields": "bold"
                }})
                break
    if bold_requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": bold_requests}
        ).execute()

    return doc_id, f"https://docs.google.com/document/d/{doc_id}/edit"


def main():
    parser = argparse.ArgumentParser(description="Generate a Ron Davis invoice")
    parser.add_argument("--month", help="Billing month in YYYY-MM format (default: all unbilled)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes made")
    args = parser.parse_args()

    from googleapiclient.discovery import build
    creds = get_credentials(SCOPES)
    sheets  = build("sheets", "v4", credentials=creds)
    docs    = build("docs", "v1", credentials=creds)
    drive   = build("drive", "v3", credentials=creds)

    # Read unbilled rows
    rows = read_unbilled_rows(sheets, month_filter=args.month)
    if not rows:
        print("No unbilled hours found.")
        return

    # Calculate totals
    total_hours = 0.0
    for _, row in rows:
        try:
            total_hours += float(row[3])
        except (ValueError, IndexError):
            pass
    total_amount = total_hours * RATE

    # Billing period label
    dates = []
    from datetime import datetime
    for _, row in rows:
        try:
            dates.append(datetime.strptime(row[0], "%b %d, %Y"))
        except (ValueError, IndexError):
            pass
    if dates:
        billing_period = f"{min(dates).strftime('%B %d')}–{max(dates).strftime('%B %d, %Y')}"
    else:
        billing_period = args.month or "All unbilled"

    invoice_num = get_next_invoice_number(sheets)
    invoice_date = date.today()

    print(f"\nInvoice Preview:")
    print(f"  Invoice #:      INV-DAVIS-{invoice_num:03d}")
    print(f"  Invoice Date:   {invoice_date.strftime('%B %d, %Y')}")
    print(f"  Billing Period: {billing_period}")
    print(f"  Rows:           {len(rows)}")
    print(f"  Total Hours:    {total_hours:.2f}")
    print(f"  Total Amount:   ${total_amount:,.2f}")

    if args.dry_run:
        print("\n[Dry run — no changes made.]")
        return

    print("\nCreating invoice doc...")
    doc_id, doc_url = create_invoice_doc(
        docs, drive, invoice_num, invoice_date,
        billing_period, rows, total_hours, total_amount
    )

    print("Marking rows as billed...")
    row_indices = [idx for idx, _ in rows]
    mark_rows_billed(sheets, row_indices, f"INV-DAVIS-{invoice_num:03d}")
    save_invoice_number(sheets, invoice_num)

    print(f"\nDone.")
    print(f"Invoice: {doc_url}")


if __name__ == "__main__":
    main()
