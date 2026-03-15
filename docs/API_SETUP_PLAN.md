# Google Workspace API Setup — Nathan's Checklist

This is the step-by-step guide for setting up Claude's Google Workspace access in the candidette repo. Nathan runs this, ideally on a screen-share call with Liz.

**Time estimate**: 15-20 minutes

---

## A. Create Google Cloud Project (under Liz's account)

1. Sign in as Liz at [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project dropdown (top bar) → **New Project**
3. Project name: `candidette-workspace`
4. Click **Create**
5. Select the new project from the dropdown

## B. Enable APIs

In the new project, go to **APIs & Services → Library** and enable:

- [x] Google Sheets API
- [x] Google Docs API
- [x] Google Calendar API
- [x] Google Drive API

Search for each one and click **Enable**.

## C. Create Service Account

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → Service Account**
3. Service account name: `claude-assistant`
4. Service account ID will auto-fill (e.g., `claude-assistant@candidette-workspace.iam.gserviceaccount.com`)
5. Click **Create and Continue**
6. Skip the "Grant this service account access" step (no project-level roles needed)
7. Skip the "Grant users access" step
8. Click **Done**

## D. Download Key

1. Click on the new service account in the list
2. Go to **Keys** tab
3. Click **Add Key → Create new key**
4. Choose **JSON**
5. Download the file
6. Save it as: `candidette/config/google_credentials.json`

**IMPORTANT**: This file is already gitignored (`config/*.json`). Never commit it.

## E. Note the Service Account Email

Copy the email address (looks like `claude-assistant@candidette-workspace.iam.gserviceaccount.com`). You'll need this to share resources.

After setup, paste it into `config/sheets.yaml` in the `service_account_email` field so Claude sessions always know it.

---

## F. Share Google Resources with Service Account

The service account can only access resources explicitly shared with it. Share things the same way you'd share with a person:

### Sheets & Docs
1. Open the Sheet or Doc
2. Click **Share**
3. Paste the service account email
4. Set permission to **Editor** (for read+write) or **Viewer** (read only)
5. Uncheck "Notify people" (it's a robot, not a person)
6. Click **Share**

### Calendar
1. Open Google Calendar (as Liz)
2. Hover over the calendar in the left sidebar → three dots → **Settings and sharing**
3. Scroll to **Share with specific people or groups**
4. Click **Add people and groups**
5. Paste the service account email
6. Set permission to **Make changes to events**
7. Click **Send**

### Drive Folders
1. Right-click the folder in Google Drive
2. Click **Share**
3. Paste the service account email
4. Set to **Editor**
5. Click **Share**

---

## G. Install Python Dependencies (on Liz's machine)

```bash
# Verify Python is available (macOS usually has it)
python3 --version

# If missing, install via Homebrew or Xcode command line tools:
# xcode-select --install
# OR
# brew install python

# Install dependencies
cd /path/to/candidette
python3 -m pip install -r scripts/requirements.txt
```

## H. Smoke Test

```bash
cd /path/to/candidette

# Test with a Sheet you've already shared with the service account
python3 scripts/sheets_read.py --test

# Should print: "Connected successfully. Service account: claude-assistant@..."
```

If the test fails:
- Check that `config/google_credentials.json` exists and is the right file
- Check that the Sheets API is enabled in the GCP project
- Check that the test Sheet is shared with the service account email

---

## I. Fill in Resource Registry

Edit `config/sheets.yaml` and replace placeholder IDs with real ones:

1. Open each Sheet/Doc Liz uses → copy the ID from the URL
   - Sheet URL: `https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit`
   - Doc URL: `https://docs.google.com/document/d/THIS_IS_THE_ID/edit`
2. Update `config/sheets.yaml` with the real IDs and descriptions
3. Add Liz's calendar email to the calendars section

---

## Credential Rotation (Future)

If the key is ever compromised:
1. Go to GCP Console → Credentials → Service Account → Keys
2. Delete the old key
3. Create a new one
4. Replace `config/google_credentials.json` on Liz's machine
5. No code changes needed — everything reads from the same path
