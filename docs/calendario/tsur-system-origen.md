# Origen y linaje del Sistema Tsur (Tsurlug)

Este documento fija qué entendemos por “sistema Tsur/Tsurlug” en Tsurphu y cuál es la cadena de linaje y textos que tomamos como referencia para el motor de calendario.

---

## 1. Contexto general

En el mundo tibetano hay varias tradiciones de calendario. Dos de las más importantes son:

- la tradición **Phuk** (Phugpa),
- la tradición **Tsur/Tsurphu (Tsurlug)**, asociada a la escuela **Karma Kagyu**.

Tsurphu (Tsurlug) es el sistema que Tsurphu (el software) adopta como base para:

- convertir fechas tibetanas ↔ gregorianas,
- obtener los signos de año/mes/día/hora,
- calcular mewa y parkha,
- identificar tipos de día (skylight arches, días especiales, etc.).

---

## 2. Cadena de linaje del sistema Tsur

### 2.1. Orígenes

1. **3er Karmapa, Rangjung Dorje (1284–1339)**  
   Tras realizar el significado último del tantra del Adibuddha, en particular del Kālacakra, compone el tratado **Tsikun Dupa** (“The Calculation of Life that Includes All”).  
   Este texto es la base fundacional del sistema Tsur de cálculo de vida y calendario.

2. **2º Pawo Rinpoché, Tsuglag Trengwa (1504–1566)**  
   Escribe un comentario extenso al Tsikun Dupa, ampliando y sistematizando el método.

### 2.2. Desarrollo y expansión

3. **7º Karmapa, Chödrak Gyamtso (1454–1506)**  
   En su época, el erudito de Tsurphu **Jamyang Chenmo Döndrup Öser**:
   - añade instrucciones al tratado del 3er Karmapa,
   - desarrolla las tablas fundamentales para los cálculos anuales del calendario.  
   Desde este momento el sistema Tsur empieza a difundirse ampliamente.

4. **Karma Ngeleg Tendzin** (discípulo principal del 8º Tai Situ, Chökyi Jungne, 1700–1774)  
   Compone numerosos tratados sobre sistemas de cálculo (calendario, astrología horaria, otros métodos de pronóstico).  
   Entre ellos destaca el **Tsishung Nyerkho Bumsang**, tratado mayor sobre estos cálculos.

### 2.3. Refinamiento y aplicación moderna

5. **Jamgön Kongtrul el Grande, Lodrö Thayé (1813–1899)**  
   Completa la compilación del manual **Tsishung Legshey Kuntu**, que había quedado inconcluso.  
   Gracias a esto, muchos eruditos pueden utilizar el sistema astrológico Tsur de manera práctica.

6. **15º Karmapa, Kakyab Dorje (1871–1922)**  
   **16º Karmapa, Rangjung Rigpe Dorje (1924–1981)**  
   El maestro de cálculos de la corte, **Ketcho Öser Rabten**:
   - introduce un nuevo enfoque en el sistema Tsur,
   - compila los datos esenciales para los almanaques astrológicos anuales.

7. **17º Karmapa, Trinley Thaye Dorje (n. 1983)**  
   Bajo sus instrucciones, el **Karma Kagyu Calendar** se calcula según el sistema Tsur desde el Losar del año 2146 (5 de febrero de 2019 en calendario occidental).

---

## 3. Textos que Tsurphu toma como referencia

Para el motor de calendario de Tsurphu consideramos como referencias tradicionales principales:

1. **Tsikun Dupa** (3er Karmapa, Rangjung Dorje) – núcleo conceptual de cálculo de vida y calendario.  
2. **Comentario de Pawo Tsuglag Trengwa** – expansión y clarificación del Tsikun Dupa.  
3. **Tablas y comentarios de Jamyang Chenmo Döndrup Öser** – base de las tablas anuales.  
4. **Tsishung Nyerkho Bumsang** (Karma Ngeleg Tendzin) – tratado mayor de sistemas de cálculo.  
5. **Tsishung Legshey Kuntu** (compilado por Jamgön Kongtrul el Grande) – manual de uso del sistema astrológico Tsur.

En la práctica moderna usaremos el **Karma Kagyu Calendar** (web y app) como referencia para:

- fechas tibetanas ↔ gregorianas,
- días especiales (parinirvanas, Guru Rinpoche days, etc.),
- tipos de día (skylight arch).

---

## 4. Decisiones de diseño en Tsurphu (software)

### 4.1. Tradición de calendario

> Tsurphu (el software) adopta explícitamente la tradición **Tsur/Tsurlug** de cálculo calendarial, tal como se describe en el linaje Karma Kagyu y se implementa en el Karma Kagyu Calendar desde 2019.

### 4.2. Jerarquía de fuentes

En caso de discrepancia entre implementaciones modernas:

1. Prima la coherencia interna de los textos tradicionales (Tsikun Dupa, comentarios, Tsishung…).  
2. Entre implementaciones contemporáneas, usamos como “oráculo práctico”:
   - el Karma Kagyu Calendar como primera referencia.

### 4.3. Tests de regresión

El motor de calendario de Tsurphu deberá pasar una batería de tests basada en:

- Fechas con alto consenso (Losar, días 10 y 15 lunares, etc.).  
- Parinirvanas y aniversarios importantes publicados por el Karma Kagyu Calendar.

Estas fechas se almacenarán en archivos de pruebas dentro de `tests/calendario/` (por ejemplo `skylight-arches-2025-2026.yml`) como casos obligatorios de verificación.
