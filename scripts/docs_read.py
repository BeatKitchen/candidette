#!/usr/bin/env python3
"""Read a Google Doc and output its content as plain text.

Usage:
    python3 docs_read.py DOC_ID
    python3 docs_read.py DOC_ID --json   # raw structural JSON

Examples:
    python3 docs_read.py 1abc...xyz
    python3 docs_read.py 1abc...xyz --json
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS

from googleapiclient.discovery import build


def read_doc_text(doc_id):
    """Read a Google Doc and return its text content."""
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)
    doc = service.documents().get(documentId=doc_id).execute()

    title = doc.get("title", "Untitled")
    print(f"# {title}\n")

    body = doc.get("body", {})
    for element in body.get("content", []):
        if "paragraph" in element:
            paragraph = element["paragraph"]
            text = ""
            for elem in paragraph.get("elements", []):
                if "textRun" in elem:
                    text += elem["textRun"]["content"]
            if text.strip():
                # Check for heading style
                style = paragraph.get("paragraphStyle", {}).get("namedStyleType", "")
                if style.startswith("HEADING"):
                    level = int(style[-1]) if style[-1].isdigit() else 2
                    print(f"{'#' * level} {text.strip()}\n")
                else:
                    print(text, end="")
        elif "table" in element:
            print("[TABLE]\n")

    return doc


def read_doc_json(doc_id):
    """Read a Google Doc and return raw JSON structure."""
    creds = get_credentials(SCOPES_DOCS)
    service = build("docs", "v1", credentials=creds)
    doc = service.documents().get(documentId=doc_id).execute()
    print(json.dumps(doc, indent=2, default=str))
    return doc


def main():
    parser = argparse.ArgumentParser(description="Read a Google Doc")
    parser.add_argument("doc_id", help="Google Doc ID (from URL)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON structure")
    args = parser.parse_args()

    if args.json:
        read_doc_json(args.doc_id)
    else:
        read_doc_text(args.doc_id)


if __name__ == "__main__":
    main()
