# El ciclo de LA (bla) según Tsurphu / Karma Kagyu

Este documento resume la explicación del **LA (bla)** y su ciclo mensual por el cuerpo según la presentación del Karma Kagyu Calendar, y define cómo Tsurphu lo modela para uso clínico/ritual.

---

## 1. Qué es el LA

En la tradición tibetana:

- El **LA (bla)** es un componente de la **fuerza vital** del individuo.
- Actúa como **enlace** entre la vida de la persona y el entorno.
- Es descrito como **luminoso** y móvil: recorre el cuerpo siguiendo un **ciclo mensual lunar**.
- Cuando está íntegro:
  - permanece dentro del cuerpo,
  - incluye las **fuerzas protectoras** personales.

El LA puede tener un **substrato externo** (montaña, colina, árbol, lago, turquesa de vida, etc.). En esos casos se conecta con la **lha** o deidad local. Dañar esos lugares se considera una amenaza directa a la vida del individuo ligado a ellos.

Cuando la fuerza vital se debilita (desmayos, colapsos, enfermedades graves), el LA puede:

- separarse del cuerpo,
- deambular por el exterior,
- ser capturado o perturbado por fuerzas hostiles (damsi, magia dañina).

Si no se realiza la práctica apropiada para restaurarlo, se dice que la persona tiene serias dificultades para sostener la vida.

Después de la muerte, el LA puede seguir rondando (por ejemplo en la tumba). No reencarna, pero puede **visitar a los vivos** y aparecer en sueños o visiones.

---

## 2. Movimiento del LA en el cuerpo

Según las enseñanzas del Kālacakra:

- En los **hombres**, el LA circula fundamentalmente por el **lado izquierdo** del cuerpo.
- En las **mujeres**, por el **lado derecho**.
- El **día 1 lunar** se sitúa en las **plantas de los pies**; a partir de ahí asciende por el cuerpo durante el mes, como una “letra luminosa”, hasta volver al punto de origen.

Durante el ciclo diario se describe, de manera esquemática:

- al amanecer, en la **vejiga**;
- al salir el sol, en el **cuello**;
- por la mañana, en **labios y nuca**;
- al mediodía, en **pecho y costillas**;
- por la tarde, en el **abdomen**;
- al anochecer, en el **corazón**;
- al atardecer, en la **espalda**;
- durante la noche, en **todo el cuerpo**.

---

## 3. Tabla mensual del ciclo de LA (días lunares 1–30)

A continuación se da la tabla estándar (Men ngak tchewa ringsel) de la localización predominante del LA según el **día lunar**. Es la base para el módulo de calendario de Tsurphu.

> Nota:
> - `all` = aplica igual a hombres y mujeres.
> - Se distingue explícitamente pie izquierdo/derecho en los días 1 y 20.

```yaml
# Esquema lógico para /data/calendario/la_cycle.yml

la_cycle:
  1:
    male:   "sole_left_foot"
    female: "sole_right_foot"
  2:
    all: "ankles"
  3:
    all: "inner_thighs"
  4:
    all: "waistline"
  5:
    all: "inside_mouth"
  6:
    all: "chest"
  7:
    all: "back"
  8:
    all: "palms"
  9:
    all: "liver"
  10:
    all: "waistline"
  11:
    all: "nose"
  12:
    all: "stomach"
  13:
    all: "shoulder_blades"
  14:
    all: "blood_vessel_above_thumbs"
  15:
    all: "whole_body"
  16:
    all: "neck"
  17:
    all: "throat"
  18:
    all: "pit_of_stomach"
  19:
    all: "ankles"
  20:
    male:   "sole_right_foot"
    female: "sole_left_foot"
  21:
    all: "big_toe"
  22:
    all: "left_shoulder_blade"
  23:
    all: "liver"
  24:
    all: "palms"
  25:
    all: "tongue"
  26:
    all: "knees"
  27:
    all: "knees"
  28:
    all: "sexual_organs"
  29:
    all: "pupils"
  30:
    all: "whole_body"

