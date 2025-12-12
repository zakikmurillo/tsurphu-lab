"""
M1-CIELO – Cielo Tsurphu (versión laboratorio)

Funciones astronómicas básicas para el resto de motores.

Implementa:

- FechaLocal: dataclass para representar una fecha/hora local.
- Coordenadas: dataclass para latitud/longitud.
- to_utc(fecha_local) -> datetime UTC.
- calcular_du(instante_utc) -> Día Juliano (JD).
- amanecer_local(fecha, coords, zona) -> datetime local aproximado del amanecer.

`amanecer_local` usa las fórmulas simplificadas de NOAA para calcular la hora de
salida del sol, suficientes para escalas humanas y para el uso calendárico del
proyecto Tsurphu.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, time, timezone, timedelta
from zoneinfo import ZoneInfo
from math import floor, sin, cos, acos, pi


# ---------------------------------------------------------------------------
# Tipos básicos
# ---------------------------------------------------------------------------


@dataclass
class FechaLocal:
    """Fecha y hora local más zona horaria."""

    fecha: date
    hora: time
    zona: str  # ejemplo: "America/Bogota"


@dataclass
class Coordenadas:
    """
    Coordenadas geográficas simples.

    latitud  > 0 en el hemisferio norte, < 0 en el sur.
    longitud > 0 al este de Greenwich, < 0 en el oeste.
    """

    latitud: float  # grados
    longitud: float  # grados


# ---------------------------------------------------------------------------
# Conversión a UTC y Día Juliano
# ---------------------------------------------------------------------------


def to_utc(fecha_local: FechaLocal) -> datetime:
    """Convierte una FechaLocal a datetime en UTC.

    Ejemplo de uso::

        f = FechaLocal(date(1967, 3, 22), time(4, 44), "America/Bogota")
        instante_utc = to_utc(f)
    """
    tz = ZoneInfo(fecha_local.zona)
    dt_local = datetime.combine(fecha_local.fecha, fecha_local.hora, tzinfo=tz)
    return dt_local.astimezone(timezone.utc)


def calcular_du(instante_utc: datetime) -> float:
    """
    Calcula el Día Juliano (JD) a partir de un instante en UTC.

    Fórmula estándar (Jean Meeus, *Astronomical Algorithms*).
    El resultado es un número de días (puede tener parte decimal).
    """
    # Aseguramos que está en UTC
    if instante_utc.tzinfo is None:
        instante_utc = instante_utc.replace(tzinfo=timezone.utc)
    else:
        instante_utc = instante_utc.astimezone(timezone.utc)

    año = instante_utc.year
    mes = instante_utc.month
    dia = instante_utc.day
    hora = instante_utc.hour
    minuto = instante_utc.minute
    segundo = instante_utc.second + instante_utc.microsecond / 1_000_000

    # Convertimos la hora a fracción de día
    frac_dia = (hora + (minuto + segundo / 60.0) / 60.0) / 24.0
    d = dia + frac_dia

    if mes <= 2:
        año -= 1
        mes += 12

    A = floor(año / 100)
    B = 2 - A + floor(A / 4)

    jd = (
        floor(365.25 * (año + 4716))
        + floor(30.6001 * (mes + 1))
        + d
        + B
        - 1524.5
    )

    return jd


# ---------------------------------------------------------------------------
# Amanecer aproximado (fórmulas NOAA)
# ---------------------------------------------------------------------------


def _dia_del_año(fecha: date) -> int:
    """Devuelve el día del año (1–366)."""

    return fecha.timetuple().tm_yday


def _eqtime_y_decl(fecha: date) -> tuple[float, float]:
    """
    Devuelve (eqtime_min, declinacion_rad).

    Basado en las fórmulas simplificadas de NOAA para la ecuación del tiempo y
    la declinación solar. Suficiente para uso calendárico general.
    """

    n = _dia_del_año(fecha)

    # gamma: posición fraccional de la órbita de la Tierra (rad)
    # Usamos hora ~12 local; el término (12-12)/24 queda en cero.
    gamma = 2.0 * pi / 365.0 * (n - 1)

    eqtime = 229.18 * (
        0.000075
        + 0.001868 * cos(gamma)
        - 0.032077 * sin(gamma)
        - 0.014615 * cos(2 * gamma)
        - 0.040849 * sin(2 * gamma)
    )

    decl = (
        0.006918
        - 0.399912 * cos(gamma)
        + 0.070257 * sin(gamma)
        - 0.006758 * cos(2 * gamma)
        + 0.000907 * sin(2 * gamma)
        - 0.002697 * cos(3 * gamma)
        + 0.00148 * sin(3 * gamma)
    )

    return eqtime, decl


def amanecer_local(fecha: date, coords: Coordenadas, zona: str) -> datetime:
    """
    Calcula la hora aproximada de amanecer local para una fecha y coordenadas.

    - `fecha`: fecha calendario (gregoriana) local.
    - `coords`: latitud/longitud en grados.
    - `zona`: zona horaria IANA, p.ej. "America/Bogota".

    Devuelve un `datetime` con tzinfo de la zona local.

    Lanza ValueError si no hay amanecer (noche polar) o si el sol permanece por
    encima del horizonte todo el día (día polar).
    """

    lat_rad = coords.latitud * pi / 180.0
    lon = coords.longitud

    eqtime, decl = _eqtime_y_decl(fecha)

    # Altura del sol en el horizonte para amanecer (incluye refracción):
    # -0.833 grados
    solar_alt = -0.833 * pi / 180.0

    cos_h = (cos(solar_alt) - sin(lat_rad) * sin(decl)) / (cos(lat_rad) * cos(decl))

    # Puede salirse ligeramente de [-1, 1] por redondeos numéricos
    if cos_h > 1.0:
        raise ValueError("No hay amanecer en esta fecha y latitud (noche polar).")
    if cos_h < -1.0:
        raise ValueError("El sol permanece sobre el horizonte todo el día (día polar).")

    ha = acos(cos_h)  # ángulo horario en radianes
    ha_deg = ha * 180.0 / pi

    # Minutos desde medianoche UTC del amanecer
    minutos_amanecer_utc = 720 - 4 * (lon + ha_deg) - eqtime

    # Ajustamos por si se sale del día (puede ser <0 o >1440)
    dia_offset, minutos_restantes = divmod(minutos_amanecer_utc, 1440.0)
    dia_offset = int(dia_offset)

    horas = int(minutos_restantes // 60)
    mins = int(minutos_restantes - horas * 60)
    segs = int(round((minutos_restantes - horas * 60 - mins) * 60))

    # Construimos datetime UTC
    fecha_base = fecha + timedelta(days=dia_offset)
    dt_utc = datetime(
        fecha_base.year,
        fecha_base.month,
        fecha_base.day,
        0,
        0,
        0,
        tzinfo=timezone.utc,
    )
    dt_utc += timedelta(hours=horas, minutes=mins, seconds=segs)

    # Convertimos a zona local
    tz_local = ZoneInfo(zona)
    return dt_utc.astimezone(tz_local)
