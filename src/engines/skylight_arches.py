from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from pathlib import Path
import re
from typing import Dict, Iterable, Optional, Set


class FixtureParseError(ValueError):
    """Error al parsear el fixture (YAML simple)."""


# Aceptamos keys tipo: padens, year_span, nyinaks, etc.
_GROUP_RE = re.compile(r"^([A-Za-z0-9_\-]+):\s*$")
_ITEM_RE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\s*$")
_META_RE = re.compile(r"^([A-Za-z0-9_\-]+):\s*(.+)\s*$")

# year_span: "YYYY-MM-DD_to_YYYY-MM-DD"
_SPAN_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})$")


@dataclass(frozen=True)
class Fixture:
    """
    Representa el fixture ya parseado.

    Requisitos por tests:
    - fx.span_start / fx.span_end (date)
    - fx.padens / fx.lutheps / fx.nyinaks / fx.yenkongs (colecciones con len())
    - fx.group_map() devuelve dict[str, set[date]]
    """
    span_start: date
    span_end: date
    groups: Dict[str, Set[date]] = field(default_factory=dict)
    meta: Dict[str, str] = field(default_factory=dict)

    # Accesos “cómodos” exigidos por los tests:
    @property
    def padens(self) -> Set[date]:
        return self.groups.get("padens", set())

    @property
    def lutheps(self) -> Set[date]:
        return self.groups.get("lutheps", set())

    @property
    def nyinaks(self) -> Set[date]:
        return self.groups.get("nyinaks", set())

    @property
    def yenkongs(self) -> Set[date]:
        return self.groups.get("yenkongs", set())

    def group_map(self) -> Dict[str, Set[date]]:
        # Los tests usan isdisjoint(), eso existe en set.
        return self.groups


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def parse_fixture_text(text: str) -> Fixture:
    """
    Parser simple (sin PyYAML) para fixtures con forma:

        year_span: "YYYY-MM-DD_to_YYYY-MM-DD"   (metadata a nivel raíz, opcional)

        padens:
          - 2025-03-09
          - 2025-03-21
        lutheps:
          - 2025-02-05

    Ignora:
    - líneas vacías
    - comentarios que empiecen con '#'
    - BOM (\\ufeff)
    """
    meta: Dict[str, str] = {}
    tmp_groups: Dict[str, list[date]] = {}
    current: Optional[str] = None

    for raw in text.splitlines():
        line = raw.lstrip("\ufeff").rstrip("\r\n")

        # vacías
        if not line.strip():
            continue

        # comentarios
        if line.lstrip().startswith("#"):
            continue

        # grupo: "padens:"
        m = _GROUP_RE.match(line)
        if m:
            current = m.group(1)
            if current in tmp_groups:
                raise FixtureParseError(f"Grupo duplicado '{current}'.")
            tmp_groups[current] = []
            continue

        # item: "- 2025-03-09"
        m = _ITEM_RE.match(line)
        if m:
            if not current:
                raise FixtureParseError("Item de lista encontrado antes de un grupo (key:).")
            s = m.group(1)
            try:
                d = date.fromisoformat(s)
            except ValueError as e:
                raise FixtureParseError(f"Fecha inválida: '{s}'") from e
            tmp_groups[current].append(d)
            continue

        # metadata raíz: "year_span: ...", SOLO si todavía no estamos dentro de un grupo
        m = _META_RE.match(line)
        if m and current is None:
            k = m.group(1)
            v = _strip_quotes(m.group(2))
            meta[k] = v
            continue

        raise FixtureParseError(f"Línea no reconocida en fixture: {raw!r}")

    # Convertimos a sets y validamos duplicados por grupo
    groups: Dict[str, Set[date]] = {}
    for g, lst in tmp_groups.items():
        if len(lst) != len(set(lst)):
            raise FixtureParseError(f"Duplicados detectados en '{g}'.")
        groups[g] = set(lst)

    # span_start/span_end: preferimos year_span si está
    if "year_span" in meta:
        m = _SPAN_RE.match(meta["year_span"])
        if not m:
            raise FixtureParseError(
                f"year_span inválido: {meta['year_span']!r} (esperado YYYY-MM-DD_to_YYYY-MM-DD)"
            )
        span_start = date.fromisoformat(m.group(1))
        span_end = date.fromisoformat(m.group(2))
    else:
        # fallback: min/max de todas las fechas
        all_dates = [d for s in groups.values() for d in s]
        if not all_dates:
            raise FixtureParseError("Fixture vacío (sin year_span y sin fechas).")
        span_start = min(all_dates)
        span_end = max(all_dates)

    return Fixture(span_start=span_start, span_end=span_end, groups=groups, meta=meta)


def load_fixture(fixture_path: Path) -> Fixture:
    # utf-8-sig elimina BOM si existe
    text = fixture_path.read_text(encoding="utf-8-sig", errors="replace")
    return parse_fixture_text(text)


@lru_cache(maxsize=16)
def _cached_load_fixture(path_str: str) -> Fixture:
    return load_fixture(Path(path_str))


def classify_date(d: date, *, fixture_path: Path) -> str:
    """
    Devuelve la etiqueta esperada por tests:
    - 'padens' -> 'paden'
    - 'lutheps' -> 'luthep'
    - 'nyinaks' -> 'nyinak'
    - 'yenkongs' -> 'yenkong'
    """
    fx = _cached_load_fixture(str(fixture_path))

    hits = [g for g, ds in fx.group_map().items() if d in ds]
    if not hits:
        return None
    if len(hits) > 1:
        raise ValueError(f"La fecha {d.isoformat()} aparece en múltiples grupos: {hits}")

    g = hits[0]
    return g[:-1] if g.endswith("s") else g
