from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import csv
from typing import Optional, Tuple

from .year_mewa_parkha import mewa_for_gregorian_year, parkha_for_mewa, year_polarity_from_stem_index

# Base estándar sexagenaria: 1984 = Wood Rat
_STEMS = ["Wood","Wood","Fire","Fire","Earth","Earth","Metal","Metal","Water","Water"]
_ANIMALS = ["Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Sheep","Monkey","Bird","Dog","Pig"]

@dataclass(frozen=True)
class TibetanYear:
    gregorian_year: int
    element: str
    animal: str
    stem_index: int
    branch_index: int
    mewa: Optional[int] = None
    parkha: Optional[str] = None

def sexagenary_from_gregorian(year: int) -> Tuple[str, str, int, int]:
    delta = year - 1984
    stem_i = delta % 10
    branch_i = delta % 12
    return _STEMS[stem_i], _ANIMALS[branch_i], stem_i, branch_i

def lookup_mewa_parkha(year: int, *, lookup_csv: Path) -> Tuple[Optional[int], Optional[str]]:
    if not lookup_csv.exists():
        return None, None
    with lookup_csv.open("r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                y = int((row.get("year") or "").strip())
            except Exception:
                continue
            if y == year:
                mewa = (row.get("mewa") or "").strip() or None
                parkha = (row.get("parkha") or "").strip() or None
                return (int(mewa) if mewa is not None else None), parkha
    return None, None

def tibetan_year(year: int, *, lookups_dir: Path | None = None) -> TibetanYear:
    element, animal, stem_i, branch_i = sexagenary_from_gregorian(year)

    # Preferir lookup (si existe y está poblado)
    mewa = parkha = None
    if lookups_dir is not None:
        csv_path = lookups_dir / "year_mewa_parkha.csv"
        mewa, parkha = lookup_mewa_parkha(year, lookup_csv=csv_path)

    # Si no hay lookup, usamos algoritmo base (para tests/pipeline)
    if mewa is None:
        mewa = mewa_for_gregorian_year(year)
    if parkha is None:
        pol = year_polarity_from_stem_index(stem_i)
        parkha = parkha_for_mewa(mewa, polarity=pol).code

    return TibetanYear(
        gregorian_year=year,
        element=element,
        animal=animal,
        stem_index=stem_i,
        branch_index=branch_i,
        mewa=mewa,
        parkha=parkha,
    )
