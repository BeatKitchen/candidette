#!/usr/bin/env python3
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path("/Users/elizabethrosenberg/Developer/candidette/scripts")))
from lib.google_auth import get_credentials, SCOPES_DOCS
from googleapiclient.discovery import build

DOC_ID = "1aE8-3ntXp55-VjMF_QHGrkC7C9IyPvomItNzhyvvjy4"

def batch(service, requests):
    service.documents().batchUpdate(
        documentId=DOC_ID, body={"requests": requests}
    ).execute()
    time.sleep(1.1)

def get_end_index(service):
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc.get("body", {}).get("content", [])
    for elem in reversed(content):
        if elem.get("endIndex"):
            return elem["endIndex"] - 1
    return 1

def main():
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)

    end = get_end_index(service)

    # Add heading
    heading = "\nA Note on the Vote Goal Methodology\n"
    batch(service, [{"insertText": {"location": {"index": end}, "text": heading}}])
    batch(service, [{"updateParagraphStyle": {
        "range": {"startIndex": end + 1, "endIndex": end + len(heading)},
        "paragraphStyle": {"namedStyleType": "HEADING_2"},
        "fields": "namedStyleType"
    }}])
    end += len(heading)

    # Add body
    body = (
        "The 18–23% target above is a general estimate drawn from crowded primary benchmarks — "
        "not a model built specifically for an 18-person field. The actual math for this race looks like this:\n\n"
        "With 75,000 total votes and 18 candidates, a perfectly equal split would give each candidate "
        "roughly 5.6% of the vote (~4,200 votes). A strong top-tier candidate typically earns 2–3x the "
        "equal share, putting the realistic range for a serious contender at 10–18%. That means the "
        "winner in a genuinely fragmented 18-person field may only need 12–16% — not 18–23%.\n\n"
        "This field also has several candidates with real name recognition and infrastructure: "
        "Verlina Reynolds-Jackson (Assemblywoman), Adrian Mapp (Mayor of Plainfield), and "
        "Shanel Robinson (Somerset County Commissioner), among others. They will pull real votes. "
        "The field will not collapse to 17 people each getting 1–2%.\n\n"
        "The vote goal should be revisited once the top-tier competition is better understood. "
        "The right target is the number Sam needs to finish first — not just to be competitive — "
        "which depends on how votes consolidate around the strongest 3–4 candidates in the field.\n"
    )
    batch(service, [{"insertText": {"location": {"index": end}, "text": body}}])
    print("Done.")

if __name__ == "__main__":
    main()
