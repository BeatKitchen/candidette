#!/usr/bin/env python3
"""Create a new Google Doc.

Usage:
    python3 docs_create.py --title "Document Title" --content "Body text here"
    python3 docs_create.py --title "SOW" --content-file path/to/content.md
    python3 docs_create.py --title "SOW" --folder FOLDER_NAME_OR_ID --content "..."

Examples:
    python3 docs_create.py --title "Sam Wang SOW" --content "Statement of Work for..."
    python3 docs_create.py --title "Meeting Notes" --folder sam_wang --content-file notes.md
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, resolve_folder_id, SCOPES_DOCS, SCOPES_DRIVE

from googleapiclient.discovery import build


def create_doc(title, content, folder_id=None):
    """Create a new Google Doc with the given title and content."""
    # Need both Docs and Drive scopes if moving to a folder
    scopes = SCOPES_DOCS + SCOPES_DRIVE if folder_id else SCOPES_DOCS
    # Drive needs write access to move file
    if folder_id:
        scopes = SCOPES_DOCS + ["https://www.googleapis.com/auth/drive"]
    creds = get_credentials(scopes)

    docs_service = build("docs", "v1", credentials=creds)

    # Create the doc
    doc = docs_service.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]

    # Insert content if provided
    if content:
        requests = [{"insertText": {"location": {"index": 1}, "text": content}}]
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()

    # Move to folder if specified
    if folder_id:
        drive_service = build("drive", "v3", credentials=creds)
        # Get current parents
        file = drive_service.files().get(fileId=doc_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))
        # Move to target folder
        drive_service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents",
        ).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"Created: {title}")
    print(f"ID: {doc_id}")
    print(f"URL: {doc_url}")
    return doc_id, doc_url


def main():
    parser = argparse.ArgumentParser(description="Create a new Google Doc")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--content", help="Document body text")
    parser.add_argument("--content-file", help="Read body text from a file")
    parser.add_argument("--folder", help="Drive folder name (from registry) or ID")
    args = parser.parse_args()

    content = args.content or ""
    if args.content_file:
        content = Path(args.content_file).read_text()

    folder_id = resolve_folder_id(args.folder) if args.folder else None
    create_doc(args.title, content, folder_id)


if __name__ == "__main__":
    main()
