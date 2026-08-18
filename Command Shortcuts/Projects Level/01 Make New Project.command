#!/bin/sh
set -e
cd "$(dirname "$0")/../.."
printf 'Project name: '
read -r PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
  printf 'No project name entered. Nothing created.
'
  exit 1
fi
./research-os project create --name "$PROJECT_NAME"
printf '
Done. You can close this window.
'
