from __future__ import annotations

from pathlib import Path
import re
from datetime import date

RE_GROUP = re.compile(r'^([A-Za-z0-9_-]+):\s*$')
RE_ITEM = re.compile(r'^\s*-\s*(\d{4}-\d{2}-\d{2})\s*$')
RE_META = re.compile(r'^([A-Za-z0-9_-]+)\s*:\s*(.+?)\s*$')
RE_YEARSPAN = re.compile(r'^(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})$')

REQUIRED_ORDER = ["padens", "lutheps", "nyinaks", "yenkongs"]

def _repo_root() -> Path:
    here = Path(__file__).resolve()
    return here.parent.parent  # tools/ -> repo root

def main() -> None:
    root = _repo_root()
    fixture_path = root / "tests" / "calendario" / "skylight-arches-2025-2026.yml"
    if not fixture_path.exists():
        raise SystemExit(f"No encuentro el fixture en: {fixture_path}")

    text = fixture_path.read_text(encoding="utf-8-sig", errors="replace")

    meta: dict[str, str] = {}
    groups: dict[str, list[str]] = {}
    current: str | None = None
    saw_any_group = False

    for raw in text.splitlines():
        line = raw.lstrip("\ufeff").rstrip("\r\n")
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue

        m = RE_GROUP.match(line)
        if m:
            current = m.group(1)
            saw_any_group = True
            groups.setdefault(current, [])
            continue

        m = RE_ITEM.match(line)
        if m and current:
            groups[current].append(m.group(1))
            continue

        # metadata raíz (antes del primer grupo)
        if not saw_any_group:
            m = RE_META.match(line)
            if m:
                k = m.group(1)
                v = m.group(2).strip()
                if (len(v) >= 2) and ((v[0] == v[-1]) and v[0] in ("'", '"')):
                    v = v[1:-1]
                meta[k] = v
                continue

        raise SystemExit(f"Línea no reconocida en fixture: {raw!r}")

    if not groups:
        raise SystemExit("No encontré ningún grupo en el fixture (¿cambió el formato?).")

    ordered = [g for g in REQUIRED_ORDER if g in groups]
    ordered += sorted([g for g in groups.keys() if g not in ordered])

    # Quita overlaps: si una fecha aparece en 2 grupos, se conserva en el primero según 'ordered'
    owner: dict[str, str] = {}
    removed: list[tuple[str, str, str]] = []

    normalized: dict[str, list[str]] = {}
    for g in ordered:
        uniq = sorted(set(groups.get(g, [])))
        keep: list[str] = []
        for d in uniq:
            if d in owner:
                removed.append((d, g, owner[d]))
                continue
            owner[d] = g
            keep.append(d)
        normalized[g] = keep

    year_span = meta.get("year_span")
    if year_span and not RE_YEARSPAN.match(year_span):
        print(f"[WARN] year_span existe pero no tiene formato YYYY-MM-DD_to_YYYY-MM-DD: {year_span!r}")
        year_span = None

    if not year_span:
        all_dates = [date.fromisoformat(d) for ds in normalized.values() for d in ds]
        if not all_dates:
            raise SystemExit("No hay fechas después de normalizar; no puedo calcular year_span.")
        year_span = f"{min(all_dates).isoformat()}_to_{max(all_dates).isoformat()}"

    for g in REQUIRED_ORDER:
        if g not in normalized:
            print(f"[WARN] El grupo requerido {g!r} no existe en el fixture.")
        elif len(normalized[g]) == 0:
            print(f"[WARN] El grupo requerido {g!r} quedó VACÍO después de quitar overlaps.")

    out_lines: list[str] = []
    out_lines.append(f'year_span: "{year_span}"')
    out_lines.append("# Auto-normalized fixture (groups + dates only; overlaps removed).")
    for g in ordered:
        out_lines.append(f"{g}:")
        for d in normalized[g]:
            out_lines.append(f"  - {d}")
        out_lines.append("")

    new_text = "\n".join(out_lines).rstrip() + "\n"

    backup = fixture_path.with_suffix(fixture_path.suffix + ".bak")
    fixture_path.replace(backup)
    fixture_path.write_text(new_text, encoding="utf-8")

    print(f"[OK] Fixture re-escrito: {fixture_path}")
    print(f"[OK] Backup guardado en: {backup}")

    if removed:
        print("\nOverlaps removidos (se conserva el primer grupo según prioridad):")
        for d, removed_from, kept_in in removed[:200]:
            print(f"  - {d}: quitado de {removed_from}, conservado en {kept_in}")
        if len(removed) > 200:
            print(f"  ... y {len(removed) - 200} más")
    else:
        print("\n[OK] No se encontraron overlaps entre grupos.")

if __name__ == "__main__":
    main()
