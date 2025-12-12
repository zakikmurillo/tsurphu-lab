"""
M2-CAL – Calendario Tsurphu (versión laboratorio)

Traduce un instante local (fecha, hora, lugar) a:

- Día Juliano (DU) usando M1-CIELO.
- Día Juliano "tibetano" (DU_tibetano) aplicando la corrección local de Henning:
    - si el instante es antes del amanecer local → DU_tibetano = DU - 1
    - si es después o igual                    → DU_tibetano = DU

La conversión completa de DU_tibetano → fecha tibetana (año/mes/día, parkha,
mewa, etc.) se delegará en un backend especializado que se implementará más
adenlante.

Esta versión define:

- TibetanDateBasic: dataclass mínima para una fecha tibetana.
- TibetanCalendarBackend: interfaz para backends concretos (Henning/TCG, etc.).
- calcular_du_tibetano: aplica la corrección de amanecer.
- calcular_fecha_tibetana_basica: orquesta todo; si no hay backend, devuelve
  solo DU_tibetano (útil para depurar).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from typing import Protocol, runtime_checkable

from tsurphu.cielo import (
    FechaLocal,
    Coordenadas,
    to_utc,
    calcular_du,
    amanecer_local,
)


# ---------------------------------------------------------------------------
# Tipos de fecha tibetana (versión básica)
# ---------------------------------------------------------------------------


@dataclass
class TibetanDateBasic:
    """
    Representación mínima de una fecha tibetana.

    Esta versión laboratorio guarda solo:
    - du_tibetano: Día Juliano corregido localmente.
    - anio/mes/dia: campos opcionales que un backend podrá rellenar después.
    """

    du_tibetano: float
    anio_tibetano: int | None = None
    mes_lunar: int | None = None
    dia_lunar: int | None = None


@runtime_checkable
class TibetanCalendarBackend(Protocol):
    """
    Interfaz para motores de calendario tibetano completos.

    Un backend real recibirá un DU_tibetano y devolverá una fecha tibetana
    completa (año/mes/día, parkha, mewa, etc.).
    """

    def from_du_tibetano(self, du_tibetano: float) -> TibetanDateBasic:  # pragma: no cover - interfaz
        ...


# ---------------------------------------------------------------------------
# Funciones principales
# ---------------------------------------------------------------------------


def calcular_du_tibetano(
    fecha_gregoriana: date,
    hora_local: time,
    zona: str,
    coords: Coordenadas,
) -> float:
    """
    Calcula el DU_tibetano aplicando la corrección local de amanecer.

    1. Construye un FechaLocal con la fecha/hora/zona.
    2. Convierte a UTC y calcula DU (M1-CIELO).
    3. Calcula la hora de amanecer_local para esa fecha y lugar.
    4. Si el instante es antes del amanecer_local → DU_tibetano = DU - 1
       Si es después o igual                      → DU_tibetano = DU
    """

    # 1. Instante local
    f_local = FechaLocal(fecha=fecha_gregoriana, hora=hora_local, zona=zona)

    # 2. A UTC + DU
    instante_utc = to_utc(f_local)
    du = calcular_du(instante_utc)

    # 3. Amanecer local (en zona local)
    amanecer = amanecer_local(fecha_gregoriana, coords, zona)

    # 4. Comparamos en zona local
    dt_local = instante_utc.astimezone(amanecer.tzinfo)

    if dt_local < amanecer:
        return du - 1.0
    else:
        return du


def calcular_fecha_tibetana_basica(
    fecha_gregoriana: date,
    hora_local: time,
    zona: str,
    coords: Coordenadas,
    backend: TibetanCalendarBackend | None = None,
) -> TibetanDateBasic:
    """
    Calcula una fecha tibetana básica a partir de un instante local.

    Si se proporciona un `backend`, se delega en él la conversión completa
    DU_tibetano → campos tibetanos. Si no, se devuelve un objeto
    `TibetanDateBasic` que solo contiene el du_tibetano, útil para depurar.
    """

    du_tib = calcular_du_tibetano(fecha_gregoriana, hora_local, zona, coords)

    if backend is None:
        return TibetanDateBasic(du_tibetano=du_tib)

    return backend.from_du_tibetano(du_tib)
