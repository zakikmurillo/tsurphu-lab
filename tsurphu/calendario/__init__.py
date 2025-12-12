"""
M2-CAL – Calendario Tsurphu (interfaz de alto nivel).

Funciones principales:

- calcular_du_tibetano:
    Aplica la corrección de amanecer (Henning) para obtener el DU_tibetano.

- calcular_fecha_tibetana_basica:
    Recibe un instante local (fecha, hora, lugar), calcula DU_tibetano
    y lo pasa a un backend que se encargará de convertirlo en fecha tibetana
    completa (cuando exista dicho backend).

También expone:

- TibetanDateBasic
- TibetanCalendarBackend (interfaz/Protocolo para backends concretos).
"""

from .m2_cal import (
    TibetanDateBasic,
    TibetanCalendarBackend,
    calcular_du_tibetano,
    calcular_fecha_tibetana_basica,
)
