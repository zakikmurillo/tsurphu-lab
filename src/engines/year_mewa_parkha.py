from __future__ import annotations
from dataclasses import dataclass

# Mewa (9 números) ciclo descendente: 1,9,8,7,6,5,4,3,2 (repite)
# Base: 1984 = mewa 1 (como en tu test)
def mewa_for_gregorian_year(year: int) -> int:
    delta = year - 1984
    m = (1 - delta) % 9
    return 9 if m == 0 else m

# Polaridad por "stem_index" (0..9) alterna: 0 yang, 1 yin, 2 yang...
def year_polarity_from_stem_index(stem_index: int) -> str:
    if stem_index % 2 == 0:
        return "yang"
    return "yin"

@dataclass(frozen=True)
class Parkha:
    code: str

# Mapeo Lo Shu -> trigramas (nombres tibetanos comunes)
# 1 Kan=Kham, 2 Kun=Khon, 3 Zhen=Zin, 4 Xun=Zon, 6 Qian=Gin, 7 Dui=Dwa, 8 Gen=Khen, 9 Li=Li
_NUM_TO_PARKHA = {
    1: "Kham",
    2: "Khon",
    3: "Zin",
    4: "Zon",
    6: "Gin",
    7: "Dwa",
    8: "Khen",
    9: "Li",
}

def parkha_for_mewa(mewa: int, *, polarity: str = "yang") -> Parkha:
    """
    Para mewa != 5: mapping directo.
    Para mewa == 5: requiere convención; por ahora:
      yang -> Gin, yin -> Khon
    (explícito para no inventar silenciosamente)
    """
    if mewa == 5:
        code = "Gin" if polarity.lower() == "yang" else "Khon"
        return Parkha(code=code)

    code = _NUM_TO_PARKHA.get(mewa)
    if not code:
        raise ValueError(f"mewa inválido: {mewa}")
    return Parkha(code=code)
