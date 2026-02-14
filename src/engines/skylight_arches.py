from __future__ import annotations

"""
Skylight Arches (Tsur/Tsurlug) — data-driven lookup (v0)

Estado actual del proyecto:
- Tenemos un set de fechas "oráculo" publicado por Karma Kagyu Calendar
  para 2025-03-01 .. 2026-02-28 (padens/lutheps/nyinaks/yenkongs).
- Aún NO tenemos (en este módulo) el algoritmo formal para derivarlo desde
  el cómputo calendárico tibetano; por ahora hacemos lookup por fixture.

Este módulo:
- Carga el fixture YAML-like (sin dependencia de PyYAML).
- Permite clasificar una fecha gregoriana como uno de los grupos conocidos.

Cuando tengamos reglas/algoritmo:
- Este módulo se convierte en "regression oracle" y/o fallback,
  y la función `classify_date()` se reimplementa algorítmicamente.
"""

from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path
import re
from typing import Iterable


_YEAR_SPAN_RE = re.compile(r'^\s*year_span\s*:\s*"(.*?)"\s*$')
_KEY_RE = re.compile(r'^\s*([A-Za-z0-9_-]+)\s*:\s*$')
_DATE_RE = re.compile(r'^\s*-\s*(\d{4}-\d{2}-\d{2})\s*$')
_ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


class FixtureParseError(ValueError):
    pass


@dataclass(frozen=True)
class SkylightFixture:
    span_start: date
    span_end: date
    padens: frozenset[date]
    lutheps: frozenset[date]
    nyinaks: frozenset[date]
    yenkongs: frozenset[date]

    def all_dates(self) -> frozenset[date]:
        return frozenset(set(self.padens) | set(self.lutheps) | set(self.nyinaks) | set(self.yenkongs))

    def group_map(self) -> dict[str, frozenset[date]]:
        return {
            "padens": self.padens,
            "lutheps": self.lutheps,
            "nyinaks": self.nyinaks,
            "yenkongs": self.yenkongs,
        }


def _parse_span(raw: str) -> tuple[date, date]:
    """
    Formato esperado (según fixture actual):
      2025-03-01_to_2026-02-28
    """
    if "_to_" not in raw:
        raise FixtureParseError(f"year_span no contiene '_to_': {raw!r}")
    a, b = raw.split("_to_", 1)
    a = a.strip()
    b = b.strip()
    if not (_ISO_DATE_RE.match(a) and _ISO_DATE_RE.match(b)):
        raise FixtureParseError(f"year_span no tiene fechas ISO: {raw!r}")
    return date.fromisoformat(a), date.fromisoformat(b)


def parse_fixture_text(text: str) -> SkylightFixture:
    """
    Parser mínimo para el fixture YAML-like.
    Soporta:
      - comentarios con '#'
      - claves: year_span, padens, lutheps, nyinaks, yenkongs
      - listas con '- YYYY-MM-DD'
    """
    span_start: date | None = None
    span_end: date | None = None

    buckets: dict[str, list[date]] = {"padens": [], "lutheps": [], "nyinaks": [], "yenkongs": []}
    current: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        m_span = _YEAR_SPAN_RE.match(line)
        if m_span:
            span_raw = m_span.group(1).strip()
            span_start, span_end = _parse_span(span_raw)
            current = None
            continue

        m_key = _KEY_RE.match(line)
        if m_key:
            key = m_key.group(1).strip()
            if key in buckets:
                current = key
            else:
                current = None  # ignoramos otras claves
            continue

        m_date = _DATE_RE.match(line)
        if m_date:
            if not current:
                # Fecha fuera de lista conocida -> ignoramos
                continue
            d = date.fromisoformat(m_date.group(1))
            buckets[current].append(d)
            continue

    if span_start is None or span_end is None:
        raise FixtureParseError("No se pudo leer year_span del fixture.")

    fx = SkylightFixture(
        span_start=span_start,
        span_end=span_end,
        padens=frozenset(buckets["padens"]),
        lutheps=frozenset(buckets["lutheps"]),
        nyinaks=frozenset(buckets["nyinaks"]),
        yenkongs=frozenset(buckets["yenkongs"]),
    )
    _validate_fixture(fx)
    return fx


def _validate_sorted_unique(name: str, dates: Iterable[date]) -> None:
    lst = list(dates)
    if len(lst) != len(set(lst)):
        raise FixtureParseError(f"Duplicados detectados en '{name}'.")
    if lst != sorted(lst):
        raise FixtureParseError(f"Fechas no ordenadas ascendentemente en '{name}'.")


def _validate_fixture(fx: SkylightFixture) -> None:
    if fx.span_end < fx.span_start:
        raise FixtureParseError("year_span inválido: end < start")

    # Valida rangos, orden y duplicados
    for group, dates in fx.group_map().items():
        _validate_sorted_unique(group, dates)
        for d in dates:
            if not (fx.span_start <= d <= fx.span_end):
                raise FixtureParseError(f"Fecha fuera de year_span: {group}: {d}")

    # Valida que no haya overlaps entre grupos
    gm = fx.group_map()
    keys = list(gm.keys())
    for i, a in enumerate(keys):
        for b in keys[i + 1 :]:
            inter = gm[a].intersection(gm[b])
            if inter:
                sample = ", ".join(sorted(str(x) for x in list(inter)[:5]))
                raise FixtureParseError(f"Overlaps entre '{a}' y '{b}': {sample}")


def default_fixture_path() -> Path:
    """
    Heurística para encontrar el fixture cuando se corre desde el repo.
    """
    here = Path(__file__).resolve()
    repo_root = here.parents[2]  # .../src/engines/file.py -> .../repo
    candidate = repo_root / "tests" / "calendario" / "skylight-arches-2025-2026.yml"
    return candidate


@lru_cache(maxsize=4)
def load_fixture(path: str | Path | None = None) -> SkylightFixture:
    p = Path(path) if path is not None else default_fixture_path()
    if not p.exists():
        raise FileNotFoundError(f"Fixture no encontrado: {p}")
    return parse_fixture_text(p.read_text(encoding="utf-8", errors="ignore"))


def classify_date(d: date, *, fixture_path: str | Path | None = None) -> str | None:
    """
    Retorna: 'paden' | 'luthep' | 'nyinak' | 'yenkong' | None
    (singular, por convención externa; el fixture está en plural)

    Si la fecha está fuera del year_span del fixture, retorna None.
    """
    fx = load_fixture(fixture_path)
    if d < fx.span_start or d > fx.span_end:
        return None

    if d in fx.padens:
        return "paden"
    if d in fx.lutheps:
        return "luthep"
    if d in fx.nyinaks:
        return "nyinak"
    if d in fx.yenkongs:
        return "yenkong"
    return None
