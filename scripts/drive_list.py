#!/usr/bin/env python3
"""List files in a shared Google Drive folder.

Usage:
    python3 drive_list.py FOLDER_NAME_OR_ID
    python3 drive_list.py FOLDER_NAME_OR_ID --type doc
    python3 drive_list.py FOLDER_NAME_OR_ID --type sheet

Examples:
    python3 drive_list.py sam_wang
    python3 drive_list.py sam_wang --type doc
    python3 drive_list.py 1abc...xyz
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, resolve_folder_id, SCOPES_DRIVE

from googleapiclient.discovery import build

MIME_TYPES = {
    "doc": "application/vnd.google-apps.document",
    "sheet": "application/vnd.google-apps.spreadsheet",
    "slides": "application/vnd.google-apps.presentation",
    "folder": "application/vnd.google-apps.folder",
    "pdf": "application/pdf",
}


def list_files(folder_id, file_type=None):
    """List files in a Drive folder."""
    creds = get_credentials(SCOPES_DRIVE)
    service = build("drive", "v3", credentials=creds)

    query = f"'{folder_id}' in parents and trashed = false"
    if file_type and file_type in MIME_TYPES:
        query += f" and mimeType = '{MIME_TYPES[file_type]}'"

    results = (
        service.files()
        .list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, modifiedTime, size)",
            orderBy="modifiedTime desc",
        )
        .execute()
    )

    files = results.get("files", [])

    if not files:
        print("No files found.")
        return []

    print(f"Files in folder ({len(files)} found):\n")

    for f in files:
        mime = f.get("mimeType", "")
        modified = f.get("modifiedTime", "")[:10]

        # Friendly type label
        if "document" in mime:
            type_label = "Doc"
        elif "spreadsheet" in mime:
            type_label = "Sheet"
        elif "presentation" in mime:
            type_label = "Slides"
        elif "folder" in mime:
            type_label = "Folder"
        elif "pdf" in mime:
            type_label = "PDF"
        else:
            type_label = mime.split(".")[-1] if "." in mime else "File"

        print(f"  [{type_label}] {f['name']}  (modified {modified})  ID: {f['id']}")

    return files


def main():
    parser = argparse.ArgumentParser(description="List files in a Google Drive folder")
    parser.add_argument("folder", help="Folder name (from registry) or ID")
    parser.add_argument("--type", choices=list(MIME_TYPES.keys()),
                        help="Filter by file type")
    args = parser.parse_args()

    folder_id = resolve_folder_id(args.folder)
    list_files(folder_id, args.type)


if __name__ == "__main__":
    main()
