#!/usr/bin/env python3
"""Insert an image into a Google Doc by uploading it to Drive first.

Usage:
    python3 docs_insert_image.py DOC_ID IMAGE_PATH

Examples:
    python3 docs_insert_image.py 1abc...xyz ../nj-voter-registration-qr.png
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, SCOPES_DOCS, SCOPES_DRIVE

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def insert_image_into_doc(doc_id, image_path):
    scopes = SCOPES_DOCS + SCOPES_DRIVE
    creds = get_credentials(scopes)

    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)

    # Upload image to Drive
    image_path = Path(image_path).resolve()
    print(f"Uploading {image_path.name} to Drive...")
    media = MediaFileUpload(str(image_path), mimetype="image/png")
    file_meta = {"name": image_path.name}
    uploaded = drive_service.files().create(
        body=file_meta, media_body=media, fields="id"
    ).execute()
    file_id = uploaded["id"]
    print(f"Uploaded, file ID: {file_id}")

    # Make it publicly readable so Docs API can fetch it
    drive_service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()

    # Small delay to let Drive propagate the permission
    time.sleep(2)

    image_url = f"https://drive.google.com/uc?id={file_id}&export=download"

    # Insert image at beginning of document
    print("Inserting image into doc...")
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {
                    "insertInlineImage": {
                        "location": {"index": 1},
                        "uri": image_url,
                        "objectSize": {
                            "height": {"magnitude": 200, "unit": "PT"},
                            "width": {"magnitude": 200, "unit": "PT"},
                        },
                    }
                }
            ]
        },
    ).execute()

    print("Done! Image inserted at the top of the document.")
    print(f"Drive file ID (you can delete it later if you want): {file_id}")


def main():
    parser = argparse.ArgumentParser(description="Insert image into a Google Doc")
    parser.add_argument("doc_id", help="Google Doc ID (from URL)")
    parser.add_argument("image_path", help="Path to the image file")
    args = parser.parse_args()
    insert_image_into_doc(args.doc_id, args.image_path)


if __name__ == "__main__":
    main()
