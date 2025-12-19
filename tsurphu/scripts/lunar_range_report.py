from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys


def _daterange(d0: dt.date, d1: dt.date):
    d = d0
    step = dt.timedelta(days=1)
    while d <= d1:
        yield d
        d += step


def _extract_json(stdout: str) -> dict:
    # Por si hay prints extra, intentamos recortar al primer { ... último }
    s = stdout.strip()
    i = s.find("{")
    j = s.rfind("}")
    if i != -1 and j != -1 and j > i:
        s = s[i : j + 1]
    return json.loads(s)


def main() -> int:
    p = argparse.ArgumentParser(description="Corre lunar_day_report en un rango de fechas y emite JSON/JSONL.")
    p.add_argument("--start", required=True, help="YYYY-MM-DD (incl.)")
    p.add_argument("--end", required=True, help="YYYY-MM-DD (incl.)")
    p.add_argument("--tz", required=True, help="Ej: -05:00")
    p.add_argument("--lat", required=True, type=float)
    p.add_argument("--lon", required=True, type=float)
    p.add_argument("--name", default="Bogota")
    p.add_argument("--country", default="CO")
    p.add_argument("--format", choices=["json", "jsonl"], default="jsonl")
    args = p.parse_args()

    d0 = dt.date.fromisoformat(args.start)
    d1 = dt.date.fromisoformat(args.end)
    rows = []

    for d in _daterange(d0, d1):
        cmd = [
            sys.executable,
            "-m",
            "tsurphu.scripts.lunar_day_report",
            "--date",
            d.isoformat(),
            "--tz",
            args.tz,
            "--lat",
            str(args.lat),
            "--lon",
            str(args.lon),
            "--name",
            args.name,
            "--country",
            args.country,
        ]

        cp = subprocess.run(cmd, capture_output=True, text=True)
        if cp.returncode != 0:
            rows.append(
                {
                    "date": d.isoformat(),
                    "ok": False,
                    "stderr_tail": (cp.stderr or "").strip()[-4000:],
                    "stdout_tail": (cp.stdout or "").strip()[-2000:],
                }
            )
            continue

        data = _extract_json(cp.stdout or "{}")
        data.setdefault("meta", {})
        data["meta"]["date"] = d.isoformat()
        data["meta"]["ok"] = True
        rows.append(data)

    if args.format == "jsonl":
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
    else:
        print(json.dumps({"meta": vars(args), "rows": rows}, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
