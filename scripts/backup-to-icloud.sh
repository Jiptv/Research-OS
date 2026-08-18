#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE_DIR="$(dirname "$ROOT_DIR")"
PROJECTS_DIR="${RESEARCH_OS_PROJECTS_DIR:-$WORKSPACE_DIR/Projects}"
DEFAULT_BACKUP_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/iCloud/UX Research"
BACKUP_DIR="${1:-${RESEARCH_OS_BACKUP_DIR:-$DEFAULT_BACKUP_DIR}}"
STATUS_FILE="$ROOT_DIR/.backup-status.json"

json_status() {
  state="$1"
  last_backup_at="$2"
  message="$3"
  started_at="${4:-}"
  finished_at="${5:-}"
  python3 - "$STATUS_FILE" "$state" "$last_backup_at" "$message" "$started_at" "$finished_at" <<'PY'
import json
import sys
from pathlib import Path

path, state, last_backup_at, message, started_at, finished_at = sys.argv[1:7]
payload = {
    "status": state,
    "last_backup_at": last_backup_at,
    "started_at": started_at,
    "finished_at": finished_at,
    "message": message,
}
Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
PY
}

previous_last_backup() {
  python3 - "$STATUS_FILE" <<'PY' 2>/dev/null || true
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if path.exists():
    print(json.loads(path.read_text()).get("last_backup_at", ""))
PY
}

LAST_BACKUP_AT="$(previous_last_backup)"
STARTED_AT="$(date '+%Y-%m-%dT%H:%M:%S')"

backup_failed() {
  status=$?
  if [ "$status" -ne 0 ]; then
    FINISHED_AT="$(date '+%Y-%m-%dT%H:%M:%S')"
    json_status "error" "$LAST_BACKUP_AT" "Backup failed with exit code $status." "$STARTED_AT" "$FINISHED_AT"
  fi
}
trap backup_failed EXIT
json_status "running" "$LAST_BACKUP_AT" "Backup to iCloud is running." "$STARTED_AT" ""

if [ "$WORKSPACE_DIR" = "$BACKUP_DIR" ]; then
  printf 'Backup destination matches the local workspace path. Choose a different destination.\n' >&2
  exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
  printf 'Could not find rsync on PATH.\n' >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"

rsync -a --delete \
  --exclude '.DS_Store' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  "$ROOT_DIR/" \
  "$BACKUP_DIR/Research OS/"

if [ -d "$PROJECTS_DIR" ]; then
  rsync -a --delete \
    --exclude '.DS_Store' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    "$PROJECTS_DIR/" \
    "$BACKUP_DIR/Projects/"
fi

FINISHED_AT="$(date '+%Y-%m-%dT%H:%M:%S')"
json_status "ok" "$FINISHED_AT" "Research OS backup updated: $BACKUP_DIR" "$STARTED_AT" "$FINISHED_AT"
trap - EXIT

printf 'Research OS backup updated:\n'
printf '  %s\n' "$BACKUP_DIR"
printf '\n'
printf 'Dashboard runtime remains local:\n'
printf '  %s\n' "$ROOT_DIR"
if [ -d "$PROJECTS_DIR" ]; then
  printf '  %s\n' "$PROJECTS_DIR"
fi
