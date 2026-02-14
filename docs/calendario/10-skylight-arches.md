# Los 10 “Skylight Arches” del sistema Tsur

Este documento describe qué son los “10 skylight arches of the cave”, cómo se usan en el Karma Kagyu Calendar y cómo los modelamos en Tsurphu.

---

## 1. Definición general

En el Karma Kagyu Calendar se habla de los **“10 Skylight Arch of the Cave”**:

- Son 10 tipos de día que se repiten cíclicamente.
- Cada día recibe:
  - un nombre (uno de los 10 skylight arches),
  - una combinación de elementos,
  - y una o varias acciones a evitar (don).

En la app del Karma Kagyu Calendar estos datos se incluyen dentro de la sección de astrología tradicional, junto con combinaciones de elementos, mewa, parkha, etc.

En Tsurphu estos skylight arches se usan como **etiquetas cualitativas** del día, que otros módulos pueden consultar (rituales, agenda, análisis de eventos).

---

## 2. Ejemplo: el día PADEN

Uno de los skylight arches más citados es **PADEN**.  
En las publicaciones del Karma Kagyu Calendar se le describe, entre otras cosas, como:

- “día desfavorable para poner Lungta o banderas de oración”,
- día asociado a una acción a evitar concreta.

Para Tsurphu, a partir de estas fuentes fijamos solo lo que es seguro:

- PADEN es un tipo de día del ciclo de skylight arches.
- Para PADEN marcamos:
  - `lungta.raising = "unfavourable"` (no recomendado levantar Lungta).
- No fijamos aún otros atributos (combinación exacta de elementos, lista completa de dones) mientras no tengamos fuentes textuales claras.

---

## 3. Modelo de datos en Tsurphu

Representamos el skylight arch del día como un bloque estructurado independiente de otros factores (animal, elemento, mewa, parkha).

### 3.1. Estructura base

```yaml
skylight_arch:
  name: <string>          # p. ej. "paden", "yenkong", etc.
  element_combo: null     # p. ej. "water-wind" cuando tengamos la fuente
  don_code: null          # código interno del don principal
  lungta:
    raising: "neutral"    # "favourable" | "neutral" | "unfavourable"
  notes_tradition: []     # lista de notas textuales
