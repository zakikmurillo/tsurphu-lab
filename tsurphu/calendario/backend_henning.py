"""
Backend Henning para M2-CAL (esqueleto).

Este módulo define la clase HenningBackend, que implementa la interfaz
TibetanCalendarBackend definida en m2_cal, pero por ahora NO realiza
la conversión completa DU_tibetano -> fecha tibetana.

Su objetivo actual es:

- fijar la estructura del backend,
- documentar los pasos que habrá que implementar,
- permitir que el resto del código lo importe sin romper nada.

Más adelante se rellenará con el algoritmo basado en:

- Henning, *Kalachakra and the Tibetan Calendar*,
- Tablas TCG (tcg1309, tcgb1302, RD2018, etc.).
"""

from __future__ import annotations

from tsurphu.calendario.m2_cal import TibetanDateBasic, TibetanCalendarBackend


class HenningBackend(TibetanCalendarBackend):
    """
    Backend de calendario tibetano basado en Henning (ESQUELETO).

    ATENCIÓN: esta versión NO implementa todavía las fórmulas tibetanas.
    Simplemente envuelve el DU_tibetano en un TibetanDateBasic sin rellenar
    año/mes/día. Es equivalente a no pasar backend, pero nos fija la interfaz.
    """

    def __init__(self, variante: str = "tsurphu") -> None:
        """
        `variante` permite, en el futuro, cambiar de "escuela" o ajustes:

        - "tsurphu": versión Tsurphu local corregida (Henning + Bogotá).
        - más adelante se podrían añadir otras variantes si es necesario.
        """
        self.variante = variante

    def from_du_tibetano(self, du_tibetano: float) -> TibetanDateBasic:
        """
        Recibe DU_tibetano (float) y devuelve un TibetanDateBasic.

        Versión actual:
        - devuelve solo du_tibetano.
        - deja anio_tibetano, mes_lunar y dia_lunar como None.

        Más adelante aquí irán:
        - el conteo desde un epoch tibetano,
        - el cálculo de año/mes/día lunar,
        - los días repetidos/omitidos, etc.
        """
        return TibetanDateBasic(du_tibetano=du_tibetano)
