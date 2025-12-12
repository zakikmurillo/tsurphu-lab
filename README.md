# tsurphu-lab-

Laboratorio público para el desarrollo del motor astronómico y calendárico de Tsurphu (Kalachakra + Sowa Rigpa).

Este repositorio contiene solo código y documentación técnica. No almacena datos clínicos ni información sensible de personas.

## Paquete `tsurphu`

Estructura actual:

- `tsurphu/__init__.py` – punto de entrada del paquete.
- `tsurphu/cielo/` – motor **M1-CIELO (Cielo Tsurphu)**.
- `tsurphu/calendario/` – motor **M2-CAL (Calendario Tsurphu)**.

### M1-CIELO

Funciones implementadas:

- `FechaLocal`, `Coordenadas`.
- `to_utc(FechaLocal)` – convierte una fecha y hora locales + zona horaria a `datetime` en UTC.
- `calcular_du(instante_utc)` – calcula el Día Juliano (JD) para un instante en UTC.
- `amanecer_local(fecha, coords, zona)` – calcula la hora aproximada de amanecer local para una fecha y unas coordenadas dadas, usando fórmulas simplificadas de NOAA.

### M2-CAL

- Define tipos para representar fechas tibetanas básicas (`TibetanDateBasic`).
- Implementa `calcular_du_tibetano`, que aplica la corrección local (Henning) usando `amanecer_local`:
  - si el instante es antes del amanecer local → `DU_tibetano = DU - 1`.
  - si es después o igual → `DU_tibetano = DU`.
- Deja preparada una interfaz de backend (`TibetanCalendarBackend`) para que, más adelante, se conecte el algoritmo completo tipo Henning/TCG que traduce `DU_tibetano` a año/mes/día tibetano, parkha, mewa, etc.

Este repo sirve como laboratorio de código para el Bloque Oriental de Tsurphu.
