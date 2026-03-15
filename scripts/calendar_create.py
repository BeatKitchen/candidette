#!/usr/bin/env python3
"""Create or update Google Calendar events.

Usage:
    python3 calendar_create.py --title "Event" --date 2026-04-01 [--time 14:00] [--duration 60]
    python3 calendar_create.py --title "Event" --date 2026-04-01 --all-day
    python3 calendar_create.py --title "Event" --date 2026-04-01 --time 14:00 --calendar liz_primary

Examples:
    # Filing deadline (all day)
    python3 calendar_create.py --title "NJ-12 Filing Deadline" --date 2026-04-07 --all-day

    # Meeting with time
    python3 calendar_create.py --title "Call with Sam" --date 2026-03-20 --time 15:00 --duration 30

    # With location and description
    python3 calendar_create.py --title "Fundraiser" --date 2026-04-15 --time 18:00 --duration 120 \
        --location "Community Center" --description "Spring fundraising event"
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.google_auth import get_credentials, resolve_calendar_id, SCOPES_CALENDAR

from googleapiclient.discovery import build


def create_event(calendar_id, title, date, time=None, duration=60, all_day=False,
                 location=None, description=None):
    """Create a calendar event."""
    creds = get_credentials(SCOPES_CALENDAR)
    service = build("calendar", "v3", credentials=creds)

    if all_day:
        event_body = {
            "summary": title,
            "start": {"date": date},
            "end": {"date": date},
        }
    else:
        if not time:
            time = "09:00"
        start_dt = datetime.fromisoformat(f"{date}T{time}:00")
        end_dt = start_dt + timedelta(minutes=duration)

        event_body = {
            "summary": title,
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "America/New_York",  # Liz is East Coast
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "America/New_York",
            },
        }

    if location:
        event_body["location"] = location
    if description:
        event_body["description"] = description

    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()

    print(f"Created event: {title}")
    print(f"Date: {date}" + (f" at {time}" if time and not all_day else " (all day)"))
    if location:
        print(f"Location: {location}")
    print(f"Link: {event.get('htmlLink', 'N/A')}")
    return event


def main():
    parser = argparse.ArgumentParser(description="Create a Google Calendar event")
    parser.add_argument("--title", required=True, help="Event title")
    parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    parser.add_argument("--time", help="Start time (HH:MM, 24h). Omit for all-day.")
    parser.add_argument("--duration", type=int, default=60, help="Duration in minutes (default: 60)")
    parser.add_argument("--all-day", action="store_true", help="Create an all-day event")
    parser.add_argument("--location", help="Event location")
    parser.add_argument("--description", help="Event description")
    parser.add_argument("--calendar", default="primary",
                        help="Calendar name (from registry) or ID (default: primary)")
    args = parser.parse_args()

    calendar_id = resolve_calendar_id(args.calendar)
    create_event(
        calendar_id, args.title, args.date,
        time=args.time, duration=args.duration, all_day=args.all_day,
        location=args.location, description=args.description,
    )


if __name__ == "__main__":
    main()
