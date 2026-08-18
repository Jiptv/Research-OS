#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE_DIR="$(dirname "$ROOT_DIR")"
OUT_DIR="${1:-$WORKSPACE_DIR/dist}"
VERSION="$(date '+%Y%m%d-%H%M%S')"
PACKAGE_DIR="$OUT_DIR/research-os-share-$VERSION"
ZIP_FILE="$OUT_DIR/research-os-share-$VERSION.zip"

cleanup() {
  rm -rf "$PACKAGE_DIR"
}
trap cleanup EXIT

mkdir -p "$PACKAGE_DIR/UX Research"
cp "$ROOT_DIR/START_HERE.md" "$PACKAGE_DIR/START HERE - Research OS.md"
cp "$ROOT_DIR/AI_ASSISTANT_GUIDE.md" "$PACKAGE_DIR/UX Research/CLAUDE.md"
cp "$ROOT_DIR/AI_ASSISTANT_GUIDE.md" "$PACKAGE_DIR/UX Research/AGENTS.md"

rsync -a \
  --exclude '.DS_Store' \
  --exclude '.git/' \
  --exclude '.backup-status.json' \
  --exclude '.dashboard-settings.json' \
  --include '.env.example' \
  --exclude '.env' \
  --exclude '.env.*' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --include 'branding/' \
  --include 'branding/README.md' \
  --include 'branding/.gitignore' \
  --include 'branding/.gitkeep' \
  --exclude 'branding/*' \
  --exclude 'local-branding/***' \
  --exclude 'assets/*logo.png' \
  --exclude 'assets/*footer.png' \
  --exclude '08-looped-learning/active-learnings.md' \
  --exclude '08-looped-learning/feedback-signals.jsonl' \
  --exclude '08-looped-learning/learning-loop-state.json' \
  --exclude '08-looped-learning/review-decisions.json' \
  --exclude '08-looped-learning/suggested-learnings.md' \
  --exclude 'Command Shortcuts/Projects/' \
  --exclude 'Command Shortcuts/Rounds/' \
  --exclude 'Command Shortcuts/RESTORE.md' \
  "$ROOT_DIR/" \
  "$PACKAGE_DIR/UX Research/Research OS/"

mkdir -p "$PACKAGE_DIR/UX Research/Projects"

(
  cd "$PACKAGE_DIR"
  zip -qr "$ZIP_FILE" "START HERE - Research OS.md" "UX Research"
)

printf 'Created share package:\n'
printf '  %s\n' "$ZIP_FILE"
