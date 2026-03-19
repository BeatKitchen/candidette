#!/bin/bash
# Monthly invoice runner — called by cron on the 1st of each month at 9 AM
# Logs output to scripts/invoice_log.txt

REPO="/Users/elizabethrosenberg/Developer/candidette"
LOG="$REPO/scripts/invoice_log.txt"
PYTHON="/usr/local/bin/python3"

echo "---" >> "$LOG"
echo "$(date): Running invoice generation..." >> "$LOG"

cd "$REPO" && "$PYTHON" scripts/invoice_generate.py >> "$LOG" 2>&1

echo "$(date): Done." >> "$LOG"
