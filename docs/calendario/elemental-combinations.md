# Elemental Combinations (Tsurphu / Karma Kagyu)

Este documento resume las **10 combinaciones elementales** (conjunctions of planets and mansions) tal como las presenta el Karma Kagyu Calendar, y cómo las usa Tsurphu como módulo de decisión para elegir días favorables o desfavorables.

---

## 1. Definición general

En el sistema Tsurphu, cada día tiene:

- un **planeta regente** con su elemento,
- una **mansión lunar** con su elemento,

y de la combinación de esos dos elementos se obtiene una de las **10 “elemental combinations”**.

Estas 10 se agrupan así:

- **3 extremadamente auspiciosas** (“excellent auspicious”),
- **3 favorables** (“good favorable”),
- **3 desfavorables** (“unfavorable”),
- **1 extremadamente desfavorable** (“vile”).

Tsurphu (software) utilizará esta clasificación como **semáforo** de fondo para sugerir o matizar acciones en un día dado (rituales, inicios de proyectos, operaciones prácticas, etc.).

---

## 2. Tabla de las 10 combinaciones

### 2.1. Tres combinaciones “excellent auspicious”

1. **Earth–Earth – NGÖDRUB** – *accomplishment*  
   - Días de **realización y estabilidad**.  
     Favorecen fundaciones, construcciones, compra de tierra, proyectos que buscan consolidar algo.

2. **Water–Water – DUTSI** – *nectar*  
   - Días que **alimentan la fuerza vital**.  
     Aptos para longevidad, empoderamientos, preparación de medicinas, matrimonio y comercio.

3. **Earth–Water o Water–Earth – LANCHÖ** – *youth*  
   - **Alegría y fortuna**.  
     Favorables para celebraciones, estrenar ropa y ornamentos, música y actividades festivas.

---

### 2.2. Tres combinaciones “good favorable”

4. **Fire–Fire – PELGYUR** – *progress*  
   - Días de **crecimiento e incremento**.  
     Potencian actividades que proveen sustento (comercio, alimentos, ropa); buenos para practicar generosidad y sembrar.

5. **Wind–Wind – PUNGCHOG** – *excellence*  
   - Favorecen que las acciones **rápidas** (viajes, práctica espiritual activa) lleguen a buen término velozmente; empujan la realización de intenciones.

6. **Fire–Wind o Wind–Fire – TOBDEN** – *powerful*  
   - Días para **reunir fuerza y hacer actividades poderosas**.  
     Aptos para oraciones, ofrendas, acciones de apaciguamiento, enriquecimiento y actividades vigorosas.

---

### 2.3. Tres combinaciones “unfavorable”

7. **Earth–Wind o Wind–Earth – MIPROD** – *deficiency*  
   - Tendencia a **merma y pérdida**.  
     Pueden asociarse con fracaso, empobrecimiento, debilitamiento y obstáculos a actividades positivas.

8. **Water–Wind o Wind–Water – MITHUN** – *discord*  
   - Días de **división y conflicto**.  
     Riesgo de desacuerdos, calumnias, rupturas de amistad y aumento de acciones que dañan la armonía.

9. **Earth–Fire o Fire–Earth – REGPA** – *burning*  
   - Favorece **obstrucción y fricción**.  
     Puede manifestarse como peleas, acciones violentas, sufrimiento y malestar.

---

### 2.4. La combinación “vile” extremadamente desfavorable

10. **Fire–Water o Water–Fire – SHIWA** – *death*  
    - La combinación más crítica.  
      Tradicionalmente se asocia con riesgo de pérdida de vitalidad y obstáculos severos en cualquier actividad; solo sería “útil” para acciones dañinas, que Tsurphu no promueve.

---

## 3. Modelado en Tsurphu (software)

### 3.1. Estructura de datos

En el motor de calendario, cada día tiene un bloque `elemental_combination`:

```yaml
elemental_combination:
  key: "earth-earth"
  tibetan_name: "ngödrub"
  category: "excellent_auspicious"   # excellent_auspicious | good_favorable | unfavorable | vile
  description_es: "Realización, cimentar, estabilizar."
  description_en: "Accomplishment, foundations, stabilisation."
