# Experimentos Tsurphu

Este directorio es un cuaderno de laboratorio muy simple:
registra casos concretos que usamos para probar los motores
M1-CIELO y M2-CAL (y, más adelante, los backends tibetanos).

---

## Experimento 1 – Nacimiento de Zakik

- Nombre: Zakik Murillo
- Fecha gregoriana: 22 de marzo de 1967
- Hora local: 04:44
- Zona horaria: `America/Bogota` (UTC-5)
- Lugar: Bogotá, Colombia
- Coordenadas aproximadas: lat = +4.71, lon = −74.07

### Objetivo

1. Calcular el instante UTC con `tsurphu.cielo.to_utc`.
2. Calcular el Día Juliano DU con `tsurphu.cielo.calcular_du`.
3. Calcular la hora de amanecer local con `tsurphu.cielo.amanecer_local`.
4. Determinar el DU_tibetano con
   `tsurphu.calendario.calcular_du_tibetano(...)`:

   - si el nacimiento es antes del amanecer local → DU_tibetano = DU - 1
   - si es después o igual → DU_tibetano = DU

5. Pasar ese DU_tibetano al backend `HenningBackend`
   (cuando se implemente de verdad) para obtener:

   - año tibetano,
   - mes lunar,
   - día lunar,
   - y, más adelante, parkha y mewa.

### Estado actual

En esta fase del proyecto:

- M1-CIELO está operativo (UTC, DU, amanecer_local).
- M2-CAL calcula correctamente `DU_tibetano`.
- `HenningBackend` existe como esqueleto, pero todavía **no**
  convierte `DU_tibetano` en año/mes/día tibetano.
