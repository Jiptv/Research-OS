#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE_DIR="$(dirname "$ROOT_DIR")"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  printf 'Docker is not installed or not available on PATH. Install Docker Desktop first.\n' >&2
  exit 1
fi

mkdir -p "$WORKSPACE_DIR/Projects"

docker compose up --build -d

for _ in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS http://127.0.0.1:8765/api/health >/dev/null 2>&1; then
    printf 'Research OS dashboard: http://127.0.0.1:8765/\n'
    exit 0
  fi
  sleep 1
done

printf 'Research OS dashboard container started, but the health check did not respond yet.\n' >&2
printf 'Open http://127.0.0.1:8765/ or check logs with: docker logs research-os-dashboard\n' >&2
