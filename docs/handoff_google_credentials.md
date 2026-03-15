# Handoff: Google Credentials Blocked

**From:** Candidette session
**To:** Nathan
**Date:** 2026-03-15

## What Happened

Liz completed the Google Cloud setup through step D — created the project `candidette-workspace`, enabled all four APIs (Sheets, Docs, Calendar, Drive), and created the service account `claude-assistant@candidette-workspace.iam.gserviceaccount.com`.

Key creation was blocked by org policy:
`iam.disableServiceAccountKeyCreation`
Tracking number: `c5793172815371128`

## What's Needed

Either:
1. Disable the org policy constraint on candidette.com (requires Organization Policy Admin role), OR
2. Switch to an alternative auth approach (Workload Identity Federation, OAuth, or another method that works within the org policy)

## Service Account Email (Save This)

`claude-assistant@candidette-workspace.iam.gserviceaccount.com`

Once credentials are sorted, drop the key/credentials file at:
`config/google_credentials.json`
(already gitignored)

Then update `config/sheets.yaml` with the service account email and run the smoke test:
`python3 scripts/sheets_read.py --test`
