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
- `HenningBackend` existe como esqueleto estructural y ya se integra
  con M2-CAL, pero todavía **no** convierte `DU_tibetano` en año/mes/día
  tibetano real.

---

## Experimento 2 – Año nuevo tibetano (candidato a epoch)

> Este experimento FUTURO servirá para validar el epoch que elijamos
> para `EPOCH_TSURPHU` en el backend Henning.

### Idea general

- Seleccionar un año nuevo tibetano del sistema Phugpa/Tsurphu que:
  - esté descrito clara y explícitamente en Henning y/o TCG, y
  - tenga su correspondencia gregoriana bien establecida.

### Datos que registraremos (cuando se elija la fecha)

- Fecha tibetana del año nuevo:
  - año tibetano (número absoluto y ciclo de 60),
  - mes lunar (esperablemente 1),
  - día lunar (1),
  - sistema (Phugpa/Tsurphu).
- Fecha gregoriana correspondiente.
- Día Juliano DU (M1-CIELO).
- DU_tibetano (M2-CAL, ya corregido por amanecer local).
- Referencias textuales (Henning/TCG) donde se documenta esta fecha.

### Objetivo del experimento

1. Comprobar que, al fijar `EPOCH_TSURPHU` de acuerdo con esta fecha,
   el backend Henning puede reproducir exactamente:
   - la fecha tibetana del año nuevo,
   - y las fechas de días cercanos (día anterior y posterior).

2. Usar este experimento como primera prueba de regresión para
   cualquier cambio futuro en el algoritmo de HenningBackend.

### Estado actual

- La fecha concreta aún **no** se ha elegido; este experimento es solo
  un casillero preparado para cuando extraigamos del libro de Henning
  y de las tablas TCG un candidato sólido a epoch de validación.

---

## Experimento 3 – Fundación de Tsurphu (validación de linaje Kagyu)

> Este experimento FUTURO servirá para ver cómo el modelo tibetano de
> Tsurphu describe un hito central del linaje Kagyu: la fundación del
> monasterio de Tsurphu como asiento principal de los Karmapas.

### Idea general

- Tomar la fecha histórica de la fundación de Tsurphu como monasterio
  (sede del 1er Karmapa, Düsum Khyenpa), tal como se documenta en
  fuentes históricas modernas.
- Usar el motor Tsurphu para traducir esa fecha gregoriana a:
  - DU (M1-CIELO),
  - DU_tibetano (M2-CAL),
  - fecha tibetana (backend Henning, cuando esté implementado).

### Datos que registraremos (cuando concretemos la fecha exacta)

- Fecha histórica gregoriana (por ejemplo, año 1189, según la
  reconstrucción historiográfica que adoptemos).
- Lugar: Tsurphu (Tíbet central), con coordenadas aproximadas.
- Sistema de calendario: Phugpa/Tsurphu.
- DU (M1-CIELO) para esa fecha y lugar.
- DU_tibetano (M2-CAL), con corrección de amanecer local.
- Fecha tibetana resultante según el backend Henning
  (año tibetano, mes lunar, día lunar) cuando la lógica esté disponible.

### Objetivo del experimento

1. Observar qué patrón de año/mes/día tibetano asigna el modelo a la
   fundación de Tsurphu.
2. Usar este hito como "validación de linaje": comprobar si la
   estructura de ciclos, elementos y, más adelante, parkha y mewa,
   ofrece una lectura coherente con el carácter de Tsurphu como
   corazón del linaje Kagyu.
3. Mantener esta fecha como caso de prueba simbólico de alto valor,
   complementario a los experimentos más "técnicos" (como el Año
   Nuevo tibetano del Experimento 2).

### Estado actual

- La fecha exacta y los detalles calendáricos no se han fijado aún. Este
  experimento es un contenedor preparado para cuando el backend Henning
  esté lo suficientemente avanzado como para producir fechas tibetanas
  completas para eventos históricos.
