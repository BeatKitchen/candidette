"""Shared Google credential loader for all Candidette scripts."""

from pathlib import Path
from google.oauth2.service_account import Credentials

CREDS_PATH = Path(__file__).parent.parent.parent / "config" / "google_credentials.json"
REGISTRY_PATH = Path(__file__).parent.parent.parent / "config" / "sheets.yaml"

# Scopes for each API
SCOPES_SHEETS = ["https://www.googleapis.com/auth/spreadsheets"]
SCOPES_DOCS = ["https://www.googleapis.com/auth/documents"]
SCOPES_CALENDAR = ["https://www.googleapis.com/auth/calendar"]
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive.readonly"]


def get_credentials(scopes):
    """Load service account credentials with the given scopes."""
    if not CREDS_PATH.exists():
        raise FileNotFoundError(
            f"Credentials not found at {CREDS_PATH}\n"
            "See docs/API_SETUP_PLAN.md for setup instructions."
        )
    return Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)


def get_registry():
    """Load the resource registry (config/sheets.yaml)."""
    import yaml
    if not REGISTRY_PATH.exists():
        return {}
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f) or {}


def resolve_sheet_id(name_or_id):
    """Resolve a friendly name to a Sheet ID, or pass through if already an ID."""
    registry = get_registry()
    sheets = registry.get("sheets", {})
    if name_or_id in sheets:
        return sheets[name_or_id]["id"]
    return name_or_id


def resolve_calendar_id(name_or_id):
    """Resolve a friendly name to a Calendar ID, or pass through."""
    registry = get_registry()
    calendars = registry.get("calendars", {})
    if name_or_id in calendars:
        return calendars[name_or_id]["id"]
    return name_or_id


def resolve_folder_id(name_or_id):
    """Resolve a friendly name to a Drive folder ID, or pass through."""
    registry = get_registry()
    folders = registry.get("drive_folders", {})
    if name_or_id in folders:
        return folders[name_or_id]["id"]
    return name_or_id
