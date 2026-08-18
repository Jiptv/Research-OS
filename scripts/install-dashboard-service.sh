#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="com.research-os.dashboard"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$HOME/Library/Logs/ResearchOS"
PYTHON_BIN="$(python3 -c 'import os, sys; print(os.path.realpath(sys.executable))' 2>/dev/null || command -v python3 || true)"
DOMAIN="gui/$(id -u)"

xml_escape() {
  printf '%s' "$1" | sed \
    -e 's/&/\&amp;/g' \
    -e 's/</\&lt;/g' \
    -e 's/>/\&gt;/g'
}

if [ -z "$PYTHON_BIN" ]; then
  printf 'Could not find python3 on PATH. Install Python 3 or run ./research-os dashboard manually from Terminal.\n' >&2
  exit 1
fi

ROOT_XML="$(xml_escape "$ROOT_DIR")"
PYTHON_XML="$(xml_escape "$PYTHON_BIN")"
LOG_XML="$(xml_escape "$LOG_DIR")"

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"
: > "$LOG_DIR/dashboard.log"
: > "$LOG_DIR/dashboard.err.log"

if curl -fsS "http://127.0.0.1:8765/api/dashboard" >/dev/null 2>&1; then
  printf 'A dashboard server is already responding on http://127.0.0.1:8765/.\n'
  printf 'Stop the manual dashboard process first, then rerun this installer so the service check is reliable.\n'
  exit 1
fi

if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "$DOMAIN" "$PLIST" >/dev/null 2>&1 || true
elif launchctl list "$LABEL" >/dev/null 2>&1; then
  launchctl unload "$PLIST" >/dev/null 2>&1 || true
fi

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>

  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON_XML</string>
    <string>$ROOT_XML/research_os.py</string>
    <string>dashboard</string>
    <string>--host</string>
    <string>127.0.0.1</string>
    <string>--port</string>
    <string>8765</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$ROOT_XML</string>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>$LOG_XML/dashboard.log</string>

  <key>StandardErrorPath</key>
  <string>$LOG_XML/dashboard.err.log</string>
</dict>
</plist>
PLIST

if launchctl bootstrap "$DOMAIN" "$PLIST" >/dev/null 2>&1; then
  :
else
  launchctl load "$PLIST"
fi

launchctl enable "$DOMAIN/$LABEL" >/dev/null 2>&1 || true
launchctl kickstart -k "$DOMAIN/$LABEL" >/dev/null 2>&1 || true

sleep 2

if curl -fsS "http://127.0.0.1:8765/api/dashboard" >/dev/null 2>&1; then
  printf 'Research OS dashboard service installed and running.\n'
  printf 'Dashboard: http://127.0.0.1:8765/\n'
  printf 'Logs: %s\n' "$LOG_DIR"
else
  printf 'Research OS dashboard service was installed, but it did not start successfully.\n'
  printf '\n'
  printf 'Most likely cause on macOS: background services are not allowed to read this project folder.\n'
  printf 'Current project folder:\n'
  printf '  %s\n' "$ROOT_DIR"
  printf '\n'
  printf 'Check the error log:\n'
  printf '  %s/dashboard.err.log\n' "$LOG_DIR"
  printf '\n'
  printf 'Fix options:\n'
  printf '  1. If the folder is in Documents, Desktop or iCloud Drive, grant Full Disk Access to the Python executable used by launchd:\n'
  printf '     %s\n' "$PYTHON_BIN"
  printf '  2. Or move Research OS to a local folder such as ~/Research OS, then rerun this installer.\n'
  printf '  3. Or run manually from Terminal: ./research-os dashboard\n'
  printf '\n'
  printf 'The broken service has been removed so it does not keep restarting.\n'
  launchctl unload "$PLIST" >/dev/null 2>&1 || true
  rm "$PLIST"
  exit 1
fi
