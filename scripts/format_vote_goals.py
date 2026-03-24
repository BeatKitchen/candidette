#!/usr/bin/env python3
"""Write and format the Ron Davis vote goal analysis into a shared Google Doc."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

DOC_ID = "1pUK3Re0zr0SwM08ny5S1afAGhTEpWRZbXVgSbMKwH5o"
FONT = "Arial"

SECTIONS = [
    ("Vote Goal Analysis — Ron Davis for WA State House", "title"),
    ("LD46, Position 1  |  2026 Primary Election", "subtitle"),

    ("Registered Voters — LD46", "heading1"),
    ("Total registered voters in Legislative District 46 (King County): 105,957", "table_total"),
    ("Source: Washington Secretary of State Voter Demographics Tables, February 2026.", "body"),

    ("Voter Turnout Rate — August Primary", "heading1"),
    ("Percentage of registered voters who cast a ballot in LD46 Position 1 primary elections:", "body"),
    ("Low turnout (2022, 39,518 votes)  =  37.3% of registered voters", "table_row"),
    ("Average turnout (48,727 votes avg)  =  46.0% of registered voters", "table_row"),
    ("High turnout (2020, 62,726 votes)  =  59.2% of registered voters", "table_row"),
    ("Note: Turnout percentages are calculated using the current registered voter count (105,957) as a baseline. Actual registration totals in 2020 and 2022 were slightly lower, so historical turnout rates may be modestly higher than shown.", "italic"),

    ("Methodology", "heading1"),
    ("Vote goals are calculated using the average total votes cast in LD46 Position 1 across the 2020, 2022, and 2024 state primary elections.", "body"),

    ("Historical Primary Turnout — LD46 Position 1", "heading1"),
    ("2020 Primary  —  62,726 total votes", "table_row"),
    ("2022 Primary  —  39,518 total votes", "table_row"),
    ("2024 Primary  —  43,937 total votes", "table_row"),
    ("Average Expected Turnout  —  48,727 votes", "table_total"),

    ("Historical Results — Gerry Pollet (Incumbent)", "heading1"),
    ("2020:  53,779 votes  (85.74%)", "table_row"),
    ("2022:  32,734 votes  (82.83%)", "table_row"),
    ("2024:  36,545 votes  (83.18%)", "table_row"),
    ("Average vote share:  ~83.9%", "table_total"),

    ("Vote Goals for Ron Davis — Low Turnout Scenario (~39,518, based on 2022)", "heading1"),
    ("25% of expected turnout  =  ~9,880 votes", "table_row"),
    ("30% of expected turnout  =  ~11,855 votes", "table_row"),
    ("35% of expected turnout  =  ~13,831 votes", "table_row"),
    ("40% of expected turnout  =  ~15,807 votes", "table_row"),
    ("50%+ (win primary outright)  =  ~19,759 votes", "table_total"),

    ("Vote Goals for Ron Davis — Average Turnout Scenario (~48,727)", "heading1"),
    ("25% of expected turnout  =  ~12,182 votes", "table_row"),
    ("30% of expected turnout  =  ~14,618 votes", "table_row"),
    ("35% of expected turnout  =  ~17,054 votes", "table_row"),
    ("40% of expected turnout  =  ~19,491 votes", "table_row"),
    ("50%+ (win primary outright)  =  ~24,364 votes", "table_total"),

    ("Vote Goals for Ron Davis — High Turnout Scenario (~62,726, based on 2020)", "heading1"),
    ("25% of expected turnout  =  ~15,682 votes", "table_row"),
    ("30% of expected turnout  =  ~18,818 votes", "table_row"),
    ("35% of expected turnout  =  ~21,954 votes", "table_row"),
    ("40% of expected turnout  =  ~25,090 votes", "table_row"),
    ("50%+ (win primary outright)  =  ~31,363 votes", "table_total"),

    ("August Primary: Key Considerations", "heading1"),
    ("Assuming Ron Davis and Gerry Pollet are the only two candidates on the ballot, the primary vote goal should demonstrate viability and build momentum heading into the general election.", "body"),
    ("A realistic and strong primary showing for a challenger against an entrenched incumbent is 25\u201335% of the vote.", "body"),
    ("Pollet has faced primary challengers in every recent cycle:", "body"),
    ("2020:  Eric J. Brown (R)  \u2014  8,830 votes (14.08%)", "table_row"),
    ("2022:  Hadeel Jeanne (D)  \u2014  6,244 votes (15.80%)", "table_row"),
    ("2024:  Ahndylyn Kinney (D)  \u2014  2,853 votes (6.49%)  |  Beth Daranciang (R)  \u2014  4,464 votes (10.16%)", "table_row"),
    ("Based on average and high turnout scenarios, a target primary vote goal of ~13,400\u201317,250 votes represents a strong showing for Ron Davis.", "highlight"),
    ("Final vote goals should be confirmed with the candidate and updated as the field of candidates becomes clear.", "body"),

    ("GENERAL ELECTION ANALYSIS", "section_divider"),

    ("Historical General Election Turnout — LD46 Position 1", "heading1"),
    ("2020 General Election  —  91,369 total votes", "table_row"),
    ("2022 General Election  —  62,471 total votes", "table_row"),
    ("2024 General Election  —  83,197 total votes", "table_row"),
    ("Average Expected Turnout  —  79,012 votes", "table_total"),

    ("Historical General Election Results — Gerry Pollet (Incumbent)", "heading1"),
    ("2020:  76,563 votes  (83.80%)", "table_row"),
    ("2022:  53,179 votes  (85.13%)", "table_row"),
    ("2024:  72,727 votes  (87.42%)", "table_row"),
    ("Average vote share:  ~85.4%", "table_total"),

    ("Vote Goals for Ron Davis — General Election, Low Turnout (~62,471, based on 2022)", "heading1"),
    ("50%+1 (win general)  =  ~31,236 votes", "table_row"),
    ("53% (win goal)  =  ~33,110 votes", "table_total"),

    ("Vote Goals for Ron Davis — General Election, Average Turnout (~79,012)", "heading1"),
    ("50%+1 (win general)  =  ~39,506 votes", "table_row"),
    ("53% (win goal)  =  ~41,876 votes", "table_total"),

    ("Vote Goals for Ron Davis — General Election, High Turnout (~91,369, based on 2020)", "heading1"),
    ("50%+1 (win general)  =  ~45,685 votes", "table_row"),
    ("53% (win goal)  =  ~48,426 votes", "table_total"),

    ("November General: Key Considerations", "heading1"),
    ("To win the general election, Ron Davis needs to secure a majority of votes cast. Based on Gerry Pollet\u2019s historical dominance (83\u201387% of the vote), this will require a significant shift in voter behavior.", "body"),
    ("General election challengers and their results:", "body"),
    ("2020:  Eric J. Brown (R)  \u2014  14,704 votes (16.09%)", "table_row"),
    ("2022:  Hadeel Jeanne (D)  \u2014  8,829 votes (14.13%)", "table_row"),
    ("2024:  Beth Daranciang (R)  \u2014  10,353 votes (12.44%)", "table_row"),
    ("Estimating a win goal at 53% of the vote in average and high turnout scenarios:", "body"),
    ("Average turnout (~79,012 votes):  53%  =  ~41,876 votes needed to win", "highlight"),
    ("High turnout (~91,369 votes):  53%  =  ~48,426 votes needed to win", "highlight"),
    ("Final general election vote goals should be confirmed with the candidate and updated based on primary results and evolving race dynamics.", "body"),
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
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
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
            txt(requests, index, length, FONT, 10, color={"red": 0.4, "green": 0.4, "blue": 0.4})

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

        elif style == "highlight":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 6, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }})
            requests.append({"updateTextStyle": {
                "range": {"startIndex": index, "endIndex": index + length - 1},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": FONT},
                    "fontSize": {"magnitude": 11, "unit": "PT"},
                    "bold": True,
                    "backgroundColor": {
                        "color": {"rgbColor": {"red": 1.0, "green": 0.949, "blue": 0.0}}
                    }
                },
                "fields": "weightedFontFamily,fontSize,bold,backgroundColor"
            }})

        elif style == "section_divider":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 32, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                    "borderBottom": {
                        "color": {"color": {"rgbColor": {"red": 0.0, "green": 0.0, "blue": 0.0}}},
                        "width": {"magnitude": 2, "unit": "PT"},
                        "padding": {"magnitude": 4, "unit": "PT"},
                        "dashStyle": "SOLID"
                    }
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,borderBottom"
            }})
            txt(requests, index, length, FONT, 13, bold=True)

        elif style == "body":
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

        elif style == "table_row":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 2, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                    "indentStart": {"magnitude": 18, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,indentStart"
            }})
            txt(requests, index, length, FONT, 11)

        elif style == "table_total":
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + length},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "spaceAbove": {"magnitude": 6, "unit": "PT"},
                    "spaceBelow": {"magnitude": 4, "unit": "PT"},
                    "indentStart": {"magnitude": 18, "unit": "PT"},
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow,indentStart"
            }})
            txt(requests, index, length, FONT, 11, bold=True)

        index += length

    return requests


def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

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

    requests = build_requests(SECTIONS)
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests}
    ).execute()

    print(f"Done. Open here:\nhttps://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
