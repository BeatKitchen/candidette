#!/usr/bin/env python3
"""Read upcoming events from a Google Calendar.

Usage:
    python3 calendar_read.py [CALENDAR_NAME_OR_ID] [--days N]

Examples:
    python3 calendar_read.py                     # Liz's primary calendar, next 7 days
    python3 calendar_read.py --days 14           # next 14 days
    python3 calendar_read.py liz_primary --days 30
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, resolve_calendar_id, SCOPES_CALENDAR

from googleapiclient.discovery import build


def list_events(calendar_id, days=7):
    """List upcoming events for the next N days."""
    creds = get_credentials(SCOPES_CALENDAR)
    service = build("calendar", "v3", credentials=creds)

    now = datetime.now(timezone.utc)
    time_max = now + timedelta(days=days)

    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now.isoformat(),
            timeMax=time_max.isoformat(),
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
        print(f"No events in the next {days} days.")
        return []

    print(f"Events for the next {days} days ({len(events)} found):\n")

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        summary = event.get("summary", "(No title)")
        location = event.get("location", "")

        # Format for readability
        if "T" in start:
            dt = datetime.fromisoformat(start)
            date_str = dt.strftime("%a %b %d, %I:%M %p")
        else:
            dt = datetime.fromisoformat(start)
            date_str = dt.strftime("%a %b %d (all day)")

        line = f"  {date_str} — {summary}"
        if location:
            line += f" [{location}]"
        print(line)

    return events


def main():
    parser = argparse.ArgumentParser(description="Read upcoming calendar events")
    parser.add_argument("calendar", nargs="?", default="primary",
                        help="Calendar name (from registry) or ID (default: primary)")
    parser.add_argument("--days", type=int, default=7,
                        help="Number of days to look ahead (default: 7)")
    args = parser.parse_args()

    calendar_id = resolve_calendar_id(args.calendar)
    list_events(calendar_id, args.days)


if __name__ == "__main__":
    main()
