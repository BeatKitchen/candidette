#!/usr/bin/env python3
"""Populate Sam Wang Vote Goals doc with historical turnout analysis and vote goal matrix."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path("/Users/elizabethrosenberg/Developer/candidette/scripts")))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

DOC_ID = "1aE8-3ntXp55-VjMF_QHGrkC7C9IyPvomItNzhyvvjy4"


def get_doc(service):
    return service.documents().get(documentId=DOC_ID).execute()


def get_end_index(service):
    doc = get_doc(service)
    content = doc.get("body", {}).get("content", [])
    for elem in reversed(content):
        if elem.get("endIndex"):
            return elem["endIndex"] - 1
    return 1


def batch(service, requests):
    service.documents().batchUpdate(
        documentId=DOC_ID, body={"requests": requests}
    ).execute()
    time.sleep(1.1)  # stay under 60 writes/min quota


def insert_text(service, index, text):
    batch(service, [{"insertText": {"location": {"index": index}, "text": text}}])


def apply_para_style(service, start, end, style):
    batch(service, [{
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": {"namedStyleType": style},
            "fields": "namedStyleType",
        }
    }])


def apply_text_style(service, start, end, bold=False, italic=False, font=None, font_size=None):
    style = {}
    fields = []
    if bold:
        style["bold"] = True
        fields.append("bold")
    if italic:
        style["italic"] = True
        fields.append("italic")
    if font:
        style["weightedFontFamily"] = {"fontFamily": font}
        fields.append("weightedFontFamily")
    if font_size:
        style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
        fields.append("fontSize")
    if style:
        batch(service, [{
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "textStyle": style,
                "fields": ",".join(fields),
            }
        }])


def insert_table(service, index, rows, cols):
    batch(service, [{"insertTable": {"location": {"index": index}, "rows": rows, "columns": cols}}])


def find_table_after(doc, min_index):
    """Find the first table element with startIndex >= min_index."""
    for elem in doc.get("body", {}).get("content", []):
        if elem.get("startIndex", 0) >= min_index and "table" in elem:
            return elem
    return None


def get_all_cell_paragraphs(table_element):
    """Return flat list of (row, col, paragraph_start_index) for all cells."""
    cells = []
    for r_idx, row in enumerate(table_element["table"].get("tableRows", [])):
        for c_idx, cell in enumerate(row.get("tableCells", [])):
            for para in cell.get("content", []):
                if "paragraph" in para:
                    cells.append((r_idx, c_idx, para["startIndex"]))
                    break  # one paragraph per cell is enough
    return cells


def fill_table(service, table_element, rows_data, bold_header=True):
    """Fill table cells one at a time in reverse order to avoid index shift."""
    cell_paras = get_all_cell_paragraphs(table_element)
    flat_data = [cell for row in rows_data for cell in row]
    pairs = list(zip(cell_paras, flat_data))

    # Insert in reverse order so earlier indices aren't shifted by later insertions
    for (r, c, para_start), text in reversed(pairs):
        if text:
            batch(service, [{
                "insertText": {
                    "location": {"index": para_start},
                    "text": text,
                }
            }])

    if bold_header:
        # Re-read doc to get fresh indices after all insertions
        doc = service.documents().get(documentId=DOC_ID).execute()
        fresh_table = find_table_after(doc, table_element["startIndex"])
        if fresh_table:
            fresh_cells = get_all_cell_paragraphs(fresh_table)
            header_cells = [(r, c, ps) for r, c, ps in fresh_cells if r == 0]
            style_requests = []
            for (r, c, para_start), text in zip(header_cells, rows_data[0]):
                if text:
                    style_requests.append({
                        "updateTextStyle": {
                            "range": {
                                "startIndex": para_start,
                                "endIndex": para_start + len(text),
                            },
                            "textStyle": {"bold": True},
                            "fields": "bold",
                        }
                    })
            if style_requests:
                batch(service, style_requests)


def shade_header_row(service, table_element):
    """Apply light gray background to first row cells."""
    requests = []
    for cell in table_element["table"]["tableRows"][0]["tableCells"]:
        requests.append({
            "updateTableCellStyle": {
                "tableRange": {
                    "tableCellLocation": {
                        "tableStartLocation": {"index": table_element["startIndex"]},
                        "rowIndex": 0,
                        "columnIndex": table_element["table"]["tableRows"][0]["tableCells"].index(cell),
                    },
                    "rowSpan": 1,
                    "columnSpan": 1,
                },
                "tableCellStyle": {
                    "backgroundColor": {
                        "color": {"rgbColor": {"red": 0.85, "green": 0.85, "blue": 0.85}}
                    }
                },
                "fields": "backgroundColor",
            }
        })
    if requests:
        batch(service, requests)


def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

    print("Starting. Reading doc...")
    end = get_end_index(service)
    print(f"Insert point: {end}")

    # ══════════════════════════════════════════════════════════════
    # SECTION 1: Historical Turnout
    # ══════════════════════════════════════════════════════════════

    h1 = "Historical Turnout: NJ-12 Democratic Primary\n"
    insert_text(service, end, h1)
    apply_para_style(service, end, end + len(h1), "HEADING_1")
    end += len(h1)

    body1 = (
        "The district boundaries changed after the 2020 census. "
        "The current NJ-12 has been in use since the 2022 election. "
        "The 2014–2020 figures are from the old district configuration — a slightly different geographic footprint.\n\n"
    )
    insert_text(service, end, body1)
    end += len(body1)

    # Insert table: 7 rows (header + 6 years), 4 cols
    table1_insert_at = end - 1
    insert_table(service, table1_insert_at, 7, 4)

    doc = get_doc(service)
    table1 = find_table_after(doc, table1_insert_at)
    if table1:
        fill_table(service, table1, [
            ["Year", "Total Dem Primary Votes", "Contested?", "Notes"],
            ["2014", "~39,000–40,000 (est.)", "Yes (4 candidates)", "Open seat (Holt retired); Watson Coleman 42%, Greenstein 28%, Chivukula 22%, Zwicker 7%; pre-redistricting lines"],
            ["2016", "Not retrieved", "Barely (2 candidates)", "Incumbent + token challenger; Watson Coleman 94%; pre-redistricting lines"],
            ["2018", "35,430", "No", "Uncontested; pre-redistricting lines"],
            ["2020", "91,864", "Yes (2 candidates)", "COVID all-mail primary — outlier; pre-redistricting lines"],
            ["2022", "37,440", "No", "Uncontested; current lines (first election under new map)"],
            ["2024", "50,133", "Yes (2 candidates)", "Incumbent + 1 challenger; current lines"],
        ])
        try:
            shade_header_row(service, table1)
        except Exception:
            pass  # non-critical

    end = get_end_index(service)

    note1 = "\nNote: 2020 is an outlier — the primary was moved to July and conducted almost entirely by mail due to COVID, roughly doubling typical in-person turnout. Exclude from 2026 projections. 2014 is the closest historical comparator to 2026: an open seat with multiple credible candidates. Watson Coleman won with ~16,500 votes (42%) in a 4-person field under the old district lines.\n\n"
    insert_text(service, end, note1)
    note1_start = end
    note1_end = end + len(note1)
    apply_text_style(service, note1_start, note1_end, italic=True)
    end = note1_end

    # ══════════════════════════════════════════════════════════════
    # SECTION 2: 2026 Turnout Projection
    # ══════════════════════════════════════════════════════════════

    h2 = "2026 Turnout Projection\n"
    insert_text(service, end, h2)
    apply_para_style(service, end, end + len(h2), "HEADING_1")
    end += len(h2)

    body2 = (
        "Open seat, 18 declared Democratic candidates, no incumbent. "
        "Every competitive campaign will run GOTV operations, which drives turnout up. "
        "The 2024 primary saw a 34% increase over 2022 with just two candidates on the ballot. "
        "A wide-open 18-candidate 2026 primary will push higher.\n\n"
    )
    insert_text(service, end, body2)
    end += len(body2)

    # Insert table: 4 rows (header + 3 scenarios), 2 cols
    table2_insert_at = end - 1
    insert_table(service, table2_insert_at, 4, 2)

    doc = get_doc(service)
    table2 = find_table_after(doc, table2_insert_at)
    if table2:
        fill_table(service, table2, [
            ["Scenario", "Projected Total Votes"],
            ["Conservative", "55,000"],
            ["Moderate", "65,000"],
            ["High", "75,000"],
        ])
        try:
            shade_header_row(service, table2)
        except Exception:
            pass

    end = get_end_index(service)
    insert_text(service, end, "\n\n")
    end += 2

    # ══════════════════════════════════════════════════════════════
    # SECTION 3: What Does It Take to Win?
    # ══════════════════════════════════════════════════════════════

    h3 = "What Does It Take to Win?\n"
    insert_text(service, end, h3)
    apply_para_style(service, end, end + len(h3), "HEADING_1")
    end += len(h3)

    body3 = (
        "In an 18-candidate field, no majority is required — the winner wins on plurality. "
        "Historical data from comparable crowded primaries suggests the winner typically captures 18–28% of the vote. "
        "Finishing first with 15% is possible in a worst-case fragmentation scenario, but not a bankable target. "
        "A vote goal of 20–25% is realistic.\n\n"
    )
    insert_text(service, end, body3)
    end += len(body3)

    # Insert table: 6 rows (header + 5 vote share rows), 4 cols
    table3_insert_at = end - 1
    insert_table(service, table3_insert_at, 6, 4)

    doc = get_doc(service)
    table3 = find_table_after(doc, table3_insert_at)
    if table3:
        fill_table(service, table3, [
            ["Vote Share", "Conservative (55,000)", "Moderate (65,000)", "High (75,000)"],
            ["15%", "8,250", "9,750", "11,250"],
            ["18%", "9,900", "11,700", "13,500"],
            ["20%", "11,000", "13,000", "15,000"],
            ["25%", "13,750", "16,250", "18,750"],
            ["30%", "16,500", "19,500", "22,500"],
        ])
        try:
            shade_header_row(service, table3)
        except Exception:
            pass

    end = get_end_index(service)
    insert_text(service, end, "\n\n")
    end += 2

    # ══════════════════════════════════════════════════════════════
    # SECTION 4: Recommendation
    # ══════════════════════════════════════════════════════════════

    h4 = "Recommendation\n"
    insert_text(service, end, h4)
    apply_para_style(service, end, end + len(h4), "HEADING_1")
    end += len(h4)

    rec_bold = "Target vote goal: 12,000–15,000 votes (moderate turnout scenario).\n\n"
    insert_text(service, end, rec_bold)
    apply_text_style(service, end, end + len(rec_bold), bold=True)
    end += len(rec_bold)

    rec_body = (
        "This represents approximately 18–23% of projected turnout under the moderate scenario (65,000 total votes). "
        "A campaign that reaches this target has a strong chance of winning a plurality in a fragmented 18-person field. "
        "The floor of 12,000 is the minimum to be competitive; 15,000 creates a meaningful buffer against consolidation around another candidate.\n\n"
        "Targets by turnout scenario:\n\n"
    )
    insert_text(service, end, rec_body)
    end += len(rec_body)

    # Insert scenario target table: 4 rows (header + 3 scenarios), 3 cols
    table4_insert_at = end - 1
    insert_table(service, table4_insert_at, 4, 3)

    doc = get_doc(service)
    table4 = find_table_after(doc, table4_insert_at)
    if table4:
        fill_table(service, table4, [
            ["Turnout Scenario", "Total Votes", "Target Vote Goal (18–23%)"],
            ["Conservative", "55,000", "9,900–12,650"],
            ["Moderate", "65,000", "11,700–14,950"],
            ["High", "75,000", "13,500–17,250"],
        ])
        try:
            shade_header_row(service, table4)
        except Exception:
            pass

    end = get_end_index(service)
    insert_text(service, end, "\n\n")
    end += 2

    rec_note = (
        "This analysis should be updated as the field narrows. "
        "Each candidate who drops out changes the math. "
        "If the field consolidates to 8–10 candidates, the vote goal rises.\n"
    )
    insert_text(service, end, rec_note)
    apply_text_style(service, end, end + len(rec_note), italic=True)

    print("Done. Document populated.")


if __name__ == "__main__":
    main()
