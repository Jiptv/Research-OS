#!/bin/sh
set -eu

LABEL="com.research-os.dashboard"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

if [ -f "$PLIST" ]; then
  if launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1; then
    launchctl bootout "$DOMAIN" "$PLIST" >/dev/null 2>&1 || true
  elif launchctl list "$LABEL" >/dev/null 2>&1; then
    launchctl unload "$PLIST" >/dev/null 2>&1 || true
  fi
  rm "$PLIST"
fi

printf 'Research OS dashboard service removed.\n'
