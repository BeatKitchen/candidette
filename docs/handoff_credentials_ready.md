# Handoff: Google Credentials Ready for Install

**From:** Nathan (via BKS analytics session)
**To:** Candidette session
**Date:** 2026-03-15

## What Happened

Nathan created a GCP project (`candidate-workspace-nr`) under his own account, bypassing the org policy issue on Liz's candidette.com domain. Service account created and tested successfully on Nathan's machine.

## Service Account Email

`candidate-claude@candidate-workspace-nr.iam.gserviceaccount.com`

This is already saved in `config/sheets.yaml`.

## Credential File

Nathan is AirDropping `google_credentials.json` to Liz's machine.

### Instructions for Receiving Session

1. Check `~/Downloads/` for a file named `candidate-workspace-nr-*.json` or `google_credentials.json`
2. Copy it to `config/google_credentials.json` in this repo:
   ```
   cp ~/Downloads/candidate-workspace-nr*.json config/google_credentials.json
   ```
   (adjust the source filename to match what's actually in Downloads)
3. Run the smoke test:
   ```
   python3 scripts/sheets_read.py --test
   ```
4. Expected output: `Connected successfully. Service account: candidate-claude@...`
5. Delete the file from Downloads after confirming
6. The credentials file is gitignored — it will NOT be committed

### If the file isn't in Downloads

Nathan may need to AirDrop it. Ask Liz: "Nathan should have sent a file — can you check if it came through?" If needed, Claude may need filesystem access to `~/Downloads`, `~/Desktop`, or `~/Documents` to find it.

## Next Steps After Credentials Work

Have Liz share her Google resources with the service account email:
- Open any Sheet or Doc → Share → paste the email → Editor → Share
- Calendar: Settings → Share with specific people → paste email → "Make changes to events"

Then update `config/sheets.yaml` with the resource IDs so Claude can reference them by friendly name.
