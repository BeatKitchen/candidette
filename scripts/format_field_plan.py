#!/usr/bin/env python3
"""Write and format the Ron Davis Field Plan into a shared Google Doc."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

DOC_ID = "1Sv4ctMtThALxCftoI0UYPnkU_SGJ2zmb-IOH4Dm5uGQ"
FONT = "Arial"

SECTIONS_PRE = [
    ("Ron Davis for WA State House of Representatives", "title"),
    ("LD-46, Position 1  |  Vote Goal", "subtitle"),
    ("Turnout Projections", "heading1"),
]

SECTIONS_POST = [
    ("Background", "heading1"),
    ("LD-46 votes at a slightly higher rate than the rest of the county, so I think 37% is a solid baseline to work off.", "body"),
    ("\u201cHigh turnout\u201d of 46% would be incredible, but I think it would be more likely if there were non-Democrats running or, at least, other competitive headline races.", "body"),
    ("In terms of assessing viability, I think you should aim for 35% of the vote. The Stranger\u2019s endorsement is essential and so is door knocking. Because I know you are ambitious and super motivated, I would like to propose we anticipate a 37% turnout but use the vote goal of a higher turnout election as our guide.", "body"),

    ("Voter Targeting", "heading1"),

    ("Vote Goal", "heading2"),
    ("17,054", "highlight"),

    ("Your Base Voters", "heading2"),
    ("High propensity registered Democrats who have voted for Ron\u2019s opponents in the past. I am focusing on Hadeel Jeanne\u2019s 6,244 voters in 2022.", "body"),

    ("Vote Deficit", "heading2"),
    ("17,054 \u2212 6,244 = 10,810", "body"),

    ("Persuasion Universe Size", "heading2"),
    ("32,430", "highlight"),

    ("Persuasion Universe", "heading2"),
    ("Tier 1: \u201cVoted for the Other Dem\u201d  \u2014  ~6,000 voters", "subheading"),
    ("Who are the 15% of voters who aren\u2019t voting for Gerry? How can we ID them? Can we find breadcrumbs to lead us to the folks who preferred Hadeel Jeanne or Ahndylyn Kinney?", "body"),
    ("Tier 2: \u201cAge 45 and Under Who Always Vote in Primaries\u201d", "subheading"),
    ("Universe of voters in this age range is ~55,000. Votebuilder to likely primary voters.", "body"),
    ("Tier 3: \u201cUrbanists & Renters Who Always Vote in Primaries\u201d", "subheading"),
    ("Votebuilder/ID renters who are likely primary voters. There may be overlap with Tier 2, but this should be a sizeable group.", "body"),

    ("Voter Contact Activities: April 1\u2013July 15, 2026", "heading1"),

    ("Weekly Contact Goal: ~2,163 voters", "heading2"),
    ("To reach 32,450 voters between April 1 and July 15 (15 weeks), the campaign will need to reach 2,163 voters a week. Visualizing that:", "body"),

    ("Doors", "subheading"),
    ("~500\u2013800 contacts/week for 15 weeks. It\u2019s ambitious!", "body"),
    ("2\u20133 canvasses a week / 3 hours per canvass.", "indent"),
    ("7 volunteers per canvass, knocking 40 doors per canvass.", "indent"),
    ("Need to engage Transit Riders, HON, Tech4Housing!", "indent"),
    ("Can you host a dual-canvass with Nilu?", "indent"),
    ("To supplement hosted canvasses, consider asynchronous ones \u2014 \u201cKnock the Neighborhood.\u201d Volunteers have 1 week to knock ~80 door list.", "indent"),

    ("Community Events and Meet-and-Greets", "subheading"),
    ("ID early supporters to host meet-and-greets.", "indent"),
    ("High traffic canvasses at Farmer\u2019s Markets, etc.", "indent"),

    ("Direct Mail", "subheading"),
    ("I realize this may be cost prohibitive, but I wonder if an early mailer announcing your candidacy to the tiered voters above might be worth an investment, providing you can swing it.", "body"),

    ("Special Events \u2014 High Foot Traffic Opportunities", "heading1"),
    ("Fremont Fair & Solstice Parade \u2014 June 20\u201321, 2026", "subheading"),
    ("Parade: Saturday June 20 at 1pm. One of Seattle\u2019s biggest community events. High density of LD-46 voters in attendance.", "body"),

    ("Lake City Summer Festival & Parade \u2014 August 1, 2026", "subheading"),
    ("NE 125th St between 25th Ave NE and Lake City Way NE. 10:30am\u20139pm. Core LD-46 territory.", "body"),

    ("Luminata Lantern Parade at Green Lake \u2014 September 20, 2026", "subheading"),
    ("Just outside the primary window but worth planning for. Fremont Arts Council event circling Green Lake. Strong community turnout.", "body"),

    ("High Volume Canvass Opportunities", "heading1"),
    ("Fremont Sunday Market \u2014 Every Sunday, 10am\u20134pm (year-round)", "subheading"),
    ("400 N 34th St, Seattle. Spring/summer location begins March 29.", "body"),

    ("Lake City Farmers Market \u2014 Thursdays, 3\u20137pm (June\u2013September)", "subheading"),
    ("NE 125th & 28th Ave NE, Seattle. Season runs June 4 \u2013 September 24, 2026.", "body"),
    ("June 4, 11, 18, 25", "indent"),
    ("July 2, 9, 16, 23, 30", "indent"),
    ("August 6, 13, 20, 27", "indent"),

    ("Phinney Farmers Market \u2014 Fridays, 3\u20137pm (June\u2013September)", "subheading"),
    ("6532 Phinney Ave N, Seattle. Season runs June 6 \u2013 September 26, 2026.", "body"),
    ("June 6, 13, 20, 27", "indent"),
    ("July 11, 18, 25", "indent"),
    ("August 1, 8, 15, 22, 29", "indent"),
]

TABLE_HEADERS = ["Month", "End of Month\nVoter ID Goal", "Volunteer\nRecruitment Goal*", "Major Deadlines"]
TABLE_ROWS = [
    ["April", "", "", ""],
    ["May", "", "", ""],
    ["June", "", "", ""],
    ["July", "", "", ""],
    ["August", "", "", ""],
]
FOOTNOTE = "*This is a running/cumulative tally"

PROJ_HEADERS = ["", "Average Estimate", "High Turnout Estimate"]
PROJ_ROWS = [
    ["Projected Turnout Percentage", "37%", "46%"],
    ["Current Registered Voters", "105,957", "105,957"],
    ["Projected Turnout", "39,518", "48,727"],
    ["Vote Goal (35%)", "13,831", "17,054"],
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

def build_requests(sections, start_index=1):
    requests = []
    index = start_index

    for text, style in sections:
        content = text + "\n"
        length = len(content)
        requests.append({"insertText": {"location": {"index": index}, "text": content}})

        if style == "title":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 18, bold=True)

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
            txt(requests, index, length, FONT, 11, color={"red": 0.4, "green": 0.4, "blue": 0.4})

        elif style == "heading1":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 20, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                    "borderBottom": {
                        "color": {"color": {"rgbColor": {"red": 0.0, "green": 0.0, "blue": 0.0}}},
                        "width": {"magnitude": 0.5, "unit": "PT"},
                        "padding": {"magnitude": 2, "unit": "PT"},
                        "dashStyle": "SOLID"
                    }
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,borderBottom"
            }})
            txt(requests, index, length, FONT, 10, bold=True)

        elif style == "heading2":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 12, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 11, bold=True)

        elif style == "subheading":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 10, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, FONT, 11, bold=True,
                color={"red": 0.4, "green": 0.4, "blue": 0.4})

        elif style == "highlight":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 4, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            requests.append({"updateTextStyle": {
                "range": {"startIndex": index, "endIndex": index + length - 1},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": FONT},
                    "fontSize": {"magnitude": 14, "unit": "PT"},
                    "bold": True,
                    "backgroundColor": {"color": {"rgbColor": {"red": 1.0, "green": 0.949, "blue": 0.0}}}
                },
                "fields": "weightedFontFamily,fontSize,bold,backgroundColor"
            }})

        elif style == "mono":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 2, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, "Courier New", 10)

        elif style == "mono_bold":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 2, "unit": "PT"},
                    "spaceBelow": {"magnitude": 10, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            txt(requests, index, length, "Courier New", 10, bold=True)

        elif style == "indent":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 2, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                    "indentStart": {"magnitude": 24, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,indentStart"
            }})
            txt(requests, index, length, FONT, 10,
                color={"red": 0.25, "green": 0.25, "blue": 0.25})

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
            txt(requests, index, length, FONT, 11)

        index += length

    return requests, index


def _find_table_at(doc, min_index):
    """Return (table, table_start) for the first table at or after min_index."""
    for e in doc["body"]["content"]:
        if "table" in e and e["startIndex"] >= min_index:
            return e["table"], e["startIndex"], e["endIndex"]
    # Fallback: last table
    last = None
    for e in doc["body"]["content"]:
        if "table" in e:
            last = e
    if last:
        return last["table"], last["startIndex"], last["endIndex"]
    return None, None, None


def write_table(service, doc_id, index, headers, rows, bold_last_row=False):
    """Insert a formatted table at index. Returns the end index of the table."""
    total_rows = 1 + len(rows)
    cols = len(headers)

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertTable": {
            "rows": total_rows, "columns": cols,
            "location": {"index": index}
        }}]}
    ).execute()

    # Pass 1: collect all cell inserts, sort DESCENDING so each insert
    # doesn't shift the indices of cells we haven't processed yet.
    doc = service.documents().get(documentId=doc_id).execute()
    table, table_start, table_end = _find_table_at(doc, index)

    all_rows = [headers] + rows
    inserts = []  # (cell_start, text, r_idx, c_idx)
    for r_idx, row_data in enumerate(all_rows):
        tr = table["tableRows"][r_idx]
        for c_idx, text in enumerate(row_data):
            if text:
                cs = tr["tableCells"][c_idx]["content"][0]["startIndex"]
                inserts.append((cs, text, r_idx, c_idx))

    inserts.sort(key=lambda x: x[0], reverse=True)
    insert_requests = [
        {"insertText": {"location": {"index": cs}, "text": text}}
        for cs, text, r_idx, c_idx in inserts
    ]
    service.documents().batchUpdate(documentId=doc_id, body={"requests": insert_requests}).execute()

    # Pass 2: re-fetch to get updated positions, then apply all styles.
    doc = service.documents().get(documentId=doc_id).execute()
    table, table_start, table_end = _find_table_at(doc, index)

    style_requests = []
    for r_idx, row_data in enumerate(all_rows):
        is_header = r_idx == 0
        is_last = bold_last_row and r_idx == len(all_rows) - 1
        tr = table["tableRows"][r_idx]
        for c_idx, text in enumerate(row_data):
            cell = tr["tableCells"][c_idx]
            cs = cell["content"][0]["startIndex"]
            if text:
                ce = cs + len(text)
                style_requests.append({"updateTextStyle": {
                    "range": {"startIndex": cs, "endIndex": ce},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": FONT},
                        "fontSize": {"magnitude": 10, "unit": "PT"},
                        "bold": is_header or is_last,
                        "foregroundColor": {"color": {"rgbColor": {
                            "red": 1.0 if is_header else 0.1,
                            "green": 1.0 if is_header else 0.1,
                            "blue": 1.0 if is_header else 0.1,
                        }}}
                    },
                    "fields": "weightedFontFamily,fontSize,bold,foregroundColor"
                }})
            if is_header:
                style_requests.append({"updateTableCellStyle": {
                    "tableRange": {"tableCellLocation": {
                        "tableStartLocation": {"index": table_start},
                        "rowIndex": r_idx, "columnIndex": c_idx
                    }, "rowSpan": 1, "columnSpan": 1},
                    "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {
                        "red": 0.0, "green": 0.0, "blue": 0.0
                    }}}},
                    "fields": "backgroundColor"
                }})
            elif is_last:
                style_requests.append({"updateTableCellStyle": {
                    "tableRange": {"tableCellLocation": {
                        "tableStartLocation": {"index": table_start},
                        "rowIndex": r_idx, "columnIndex": c_idx
                    }, "rowSpan": 1, "columnSpan": 1},
                    "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {
                        "red": 1.0, "green": 0.949, "blue": 0.0
                    }}}},
                    "fields": "backgroundColor"
                }})

    if style_requests:
        service.documents().batchUpdate(documentId=doc_id, body={"requests": style_requests}).execute()

    return table_end


def add_table(service, doc_id, index):
    """Insert the voter contact activities table."""
    all_data_rows = TABLE_ROWS + [["", FOOTNOTE, "", ""]]
    total_rows = 1 + len(all_data_rows)

    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertTable": {
            "rows": total_rows, "columns": 4,
            "location": {"index": index}
        }}]}
    ).execute()

    # Pass 1: collect inserts, sort DESCENDING
    doc = service.documents().get(documentId=doc_id).execute()
    table, table_start, _ = _find_table_at(doc, index)
    if not table:
        print("Table not found")
        return

    all_rows = [TABLE_HEADERS] + all_data_rows
    inserts = []
    for r_idx, row_data in enumerate(all_rows):
        for c_idx, text in enumerate(row_data):
            if text:
                cs = table["tableRows"][r_idx]["tableCells"][c_idx]["content"][0]["startIndex"]
                inserts.append((cs, text, r_idx, c_idx))

    inserts.sort(key=lambda x: x[0], reverse=True)
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [
            {"insertText": {"location": {"index": cs}, "text": text}}
            for cs, text, _, _ in inserts
        ]}
    ).execute()

    # Pass 2: re-fetch, apply styles
    doc = service.documents().get(documentId=doc_id).execute()
    table, table_start, _ = _find_table_at(doc, index)

    style_requests = []
    for r_idx, row_data in enumerate(all_rows):
        is_header = r_idx == 0
        is_footnote = r_idx == len(all_rows) - 1
        for c_idx, text in enumerate(row_data):
            cell = table["tableRows"][r_idx]["tableCells"][c_idx]
            cs = cell["content"][0]["startIndex"]
            if text:
                ce = cs + len(text)
                style_requests.append({"updateTextStyle": {
                    "range": {"startIndex": cs, "endIndex": ce},
                    "textStyle": {
                        "weightedFontFamily": {"fontFamily": FONT},
                        "fontSize": {"magnitude": 10, "unit": "PT"},
                        "bold": is_header,
                        "italic": is_footnote,
                        "foregroundColor": {"color": {"rgbColor": {
                            "red": 1.0 if is_header else 0.2,
                            "green": 1.0 if is_header else 0.2,
                            "blue": 1.0 if is_header else 0.2
                        }}}
                    },
                    "fields": "weightedFontFamily,fontSize,bold,italic,foregroundColor"
                }})
            if is_header:
                style_requests.append({"updateTableCellStyle": {
                    "tableRange": {"tableCellLocation": {
                        "tableStartLocation": {"index": table_start},
                        "rowIndex": r_idx, "columnIndex": c_idx
                    }, "rowSpan": 1, "columnSpan": 1},
                    "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {
                        "red": 0.0, "green": 0.0, "blue": 0.0
                    }}}},
                    "fields": "backgroundColor"
                }})

    if style_requests:
        service.documents().batchUpdate(documentId=doc_id, body={"requests": style_requests}).execute()


def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

    # Clear existing content
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 2) if content else 2

    if end_index > 2:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": end_index - 1}
            }}]}
        ).execute()

    # Write pre-table sections (title, subtitle, "Turnout Projections" heading)
    requests, proj_index = build_requests(SECTIONS_PRE)
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

    # Insert projections table right after the heading
    post_proj_index = write_table(service, DOC_ID, proj_index - 1, PROJ_HEADERS, PROJ_ROWS, bold_last_row=True)

    # Write post-table sections (Background through Voter Contact Activities heading)
    requests, activities_index = build_requests(SECTIONS_POST, start_index=post_proj_index)
    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

    print(f"Done. Open here:\nhttps://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
