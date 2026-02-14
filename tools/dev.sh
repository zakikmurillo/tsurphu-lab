#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo ""
echo "=== TSURPHU DEV (one-command bootstrap + tests) ==="
echo "Repo: $ROOT"
python3 -V || true

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
else
  echo ">> venv already exists: $ROOT/.venv"
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -U pip wheel setuptools

python -m pip install -e ".[dev]" 2>/dev/null || python -m pip install -e .
python -m pip install -U pytest

if [[ ! -f tools/tsurphu.py ]]; then
  echo "Missing CLI: tools/tsurphu.py" >&2
  exit 1
fi

HELP_TEXT="$(python tools/tsurphu.py -h 2>&1 || true)"

CMD=""
if echo "$HELP_TEXT" | grep -Eq '\bbootstrap\b'; then
  CMD="bootstrap"
elif echo "$HELP_TEXT" | grep -Eq '\bvalidate\b'; then
  CMD="validate"
else
  echo "No known command found in tsurphu CLI help. Expected bootstrap or validate." >&2
  exit 1
fi

python tools/tsurphu.py "$CMD"
pytest -q

echo ""
echo "=== Key files ==="
echo "Documento Maestro: $ROOT/docs/master.md"
echo "ChangeSetPacket-1: $ROOT/docs/changesetpacket-1.md"
echo "Changesets dir:    $ROOT/changesets"
echo ""
echo "DONE ✅"
