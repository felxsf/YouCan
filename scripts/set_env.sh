#!/usr/bin/env bash
set -euo pipefail
PATH_FILE="${1:-.env}"
if [ ! -f "$PATH_FILE" ]; then
  echo "Archivo no encontrado: $PATH_FILE" >&2
  exit 1
fi
while IFS= read -r line; do
  trimmed="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [ -z "$trimmed" ] && continue
  case "$trimmed" in \#*) continue ;; esac
  IFS='=' read -r key val <<< "$trimmed"
  export "$key"="$val"
done < "$PATH_FILE"
echo "Variables cargadas en la sesión actual."
