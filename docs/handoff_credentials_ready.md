# Handoff: Google Credentials Ready for Install

**From:** Nathan (via BKS analytics session)
**To:** Candidette session
**Date:** 2026-03-15

## What Happened

Nathan created a GCP project (`candidate-workspace-nr`) under his own account, bypassing the org policy issue on Liz's candidette.com domain. Service account created and tested successfully on Nathan's machine.

## Service Account Email (USE THIS ONE)

`candidate-claude@candidate-workspace-nr.iam.gserviceaccount.com`

This is already saved in `config/sheets.yaml`.

## IMPORTANT: Two Service Accounts Exist — Only One Works

Liz previously created a GCP project (`candidette-workspace`) under her candidette.com domain, with a service account:

`claude-assistant@candidette-workspace.iam.gserviceaccount.com`

**That one does NOT work** — key creation was blocked by her org policy. It's a decoy.

When Liz shares Sheets/Docs/Calendar, she must share with the **correct** email:
`candidate-claude@candidate-workspace-nr.iam.gserviceaccount.com`

**NOT** `claude-assistant@candidette-workspace.iam.gserviceaccount.com`

The two look similar. Be careful. If Liz has already shared things with the old one, she'll need to re-share with the correct one.

**Liz should also delete the old project** (`candidette-workspace`) from her GCP console to avoid confusion:
- Go to console.cloud.google.com (signed in as Liz)
- Select `candidette-workspace` from the project picker
- Settings → Shut down project
- This is optional but prevents future confusion

## Credential File

Nathan AirDropped `google_credentials.json` to Liz's machine.

### Instructions for Receiving Session

1. Check `~/Downloads/` for a file named `candidate-workspace-nr-*.json` or `google_credentials.json`
2. Copy it to `config/google_credentials.json` in this repo:
   ```
   cp ~/Downloads/candidate-workspace-nr*.json config/google_credentials.json
   ```
   (adjust the source filename to match what's actually in Downloads)
3. Install Python dependencies if not already done:
   ```
   python3 -m pip install -r scripts/requirements.txt
   ```
4. Run the smoke test:
   ```
   python3 scripts/sheets_read.py --test
   ```
5. Expected output: `Connected successfully. Service account: candidate-claude@...`
6. Delete the file from Downloads after confirming
7. The credentials file is gitignored — it will NOT be committed

### If the file isn't in Downloads

Nathan AirDropped it. Ask Liz: "Nathan sent a file over — can you check if it came through?" Claude may need filesystem access to `~/Downloads`, `~/Desktop`, or `~/Documents` to find it. Request those permissions when needed.

## Next Steps After Credentials Work

Have Liz share her Google resources with the **correct** service account email:

> `candidate-claude@candidate-workspace-nr.iam.gserviceaccount.com`

- Open any Sheet or Doc → Share → paste the email → Editor → uncheck "Notify" → Share
- Calendar: Settings → Share with specific people → paste email → "Make changes to events"

Then update `config/sheets.yaml` with the resource IDs so Claude can reference them by friendly name.
