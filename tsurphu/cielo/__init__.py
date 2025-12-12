"""
Módulo M1-CIELO (Cielo Tsurphu).

Interfaz de alto nivel del motor astronómico:

- FechaLocal, Coordenadas
- to_utc: fecha/hora local + zona horaria → datetime UTC.
- calcular_du: día universal (día juliano) para un instante dado.
- amanecer_local: hora aproximada de amanecer local para una fecha y coordenadas.

Más adelante se añadirá:
- posiciones de Sol/Luna/planetas
- info de eclipses, etc.
"""

from .m1_cielo import (
    FechaLocal,
    Coordenadas,
    to_utc,
    calcular_du,
    amanecer_local,
)
