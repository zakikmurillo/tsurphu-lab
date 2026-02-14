#!/usr/bin/env python3
from __future__ import annotations

"""
tools/skylight_arches.py

CLI auxiliar para:
- Consultar el skylight arch (lookup por fixture)
- Verificar consistencia del fixture

Ejemplos:
  python .\tools\skylight_arches.py for-date 2025-03-09
  python .\tools\skylight_arches.py verify
  python .\tools\skylight_arches.py range 2025-03-01 2025-03-31
"""

import argparse
from datetime import date, timedelta
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from engines.skylight_arches import classify_date, load_fixture  # noqa: E402


def _iso_date(s: str) -> date:
    try:
        return date.fromisoformat(s)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Fecha inválida (ISO YYYY-MM-DD): {s!r}") from e


def main() -> int:
    p = argparse.ArgumentParser(prog="skylight_arches", add_help=True)
    p.add_argument(
        "--fixture",
        default=str(REPO_ROOT / "tests" / "calendario" / "skylight-arches-2025-2026.yml"),
        help="Ruta al fixture (default: tests/calendario/skylight-arches-2025-2026.yml)",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    p_for = sub.add_parser("for-date", help="Clasifica una fecha")
    p_for.add_argument("date", type=_iso_date)

    sub.add_parser("verify", help="Valida fixture y prueba clasificación")

    p_range = sub.add_parser("range", help="Clasifica un rango [start,end]")
    p_range.add_argument("start", type=_iso_date)
    p_range.add_argument("end", type=_iso_date)

    args = p.parse_args()

    fx = load_fixture(Path(args.fixture))

    if args.cmd == "for-date":
        tag = classify_date(args.date, fixture_path=args.fixture)
        print(tag or "none")
        return 0

    if args.cmd == "verify":
        gm = fx.group_map()
        mapping = {"padens": "paden", "lutheps": "luthep", "nyinaks": "nyinak", "yenkongs": "yenkong"}
        for group, dates in gm.items():
            expected = mapping[group]
            for d in dates:
                got = classify_date(d, fixture_path=args.fixture)
                if got != expected:
                    raise SystemExit(f"Mismatch {d}: expected {expected}, got {got}")
        print("OK")
        return 0

    if args.cmd == "range":
        if args.end < args.start:
            raise SystemExit("end < start")
        d = args.start
        while d <= args.end:
            tag = classify_date(d, fixture_path=args.fixture)
            if tag:
                print(f"{d}  {tag}")
            d += timedelta(days=1)
        return 0

    raise SystemExit("unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
