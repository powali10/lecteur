# Documento de Diseño: Lecteur

> Diseñado por Gemini (product designer ex-Apple, ex-Figma)
> Fecha: 3 Junio 2026

---

## 1. Principios de Diseño

1. **La Lectura es Sagrada** — La interfaz debe desaparecer. El contenido es el rey.
2. **La Herramienta es Discreta** — Las ayudas aparecen solo cuando se invocan. El usuario controla la profundidad.
3. **Claridad y Elegancia** — Tipografía clásica, paleta contenida, espaciado generoso. Nada superfluo.
4. **Profundidad Progresiva** — Útil para un lector casual y un lingüista experto. Información en capas.

## 2. Mapa de Pantallas

| ID | Pantalla | Propósito |
|---|---|---|
| P1 | Biblioteca | Punto de entrada. Grid de libros con progreso. |
| P2 | Lector | Experiencia de lectura inmersiva. Dos columnas. |
| P3 | Flashcards | Repaso SRS (SM-2). |
| P4 | Diccionario | Referencia completa de palabras. |
| P5 | Progreso | Estadísticas y logros. |

## 3. Wireframes

### Biblioteca (Desktop)

```
+-----------------------------------------------------------+
| Lecteur                                      Ordenar v    |
+-----------------------------------------------------------+
|  [Portada]      [Portada]      [Portada]      [Portada]   |
|  Le P. Prince   L'Étranger     Fleurs du Mal  Voyage au.. |
|  Saint-Exupéry  Camus          Baudelaire     Verne       |
|  FR|ES [■■■■■■--] 80%  FR|ES [■■■-------] 25%           |
+-----------------------------------------------------------+
|  [📚]  [🃏 Flashcards]  [📖 Diccio.]  [📊 Progreso]        |
+-----------------------------------------------------------+
```

### Lector (Desktop)

```
+-----------------------------------------------------------+
| < Le Petit Prince, Cap. 1                                 |
+-----------------------------------------------------------+
|  Original (FR)                  |  Traducción (ES)        |
|---------------------------------|-------------------------|
|  J'ai donc dû choisir un autre  |  Tuve, pues, que elegir |
|  métier et j'ai appris à       |  otro oficio y aprendí  |
|  piloter des avions.            |  a pilotar aviones.     |
|                                 |                         |
|> Mais oui ! Les grandes         |  ¡Pues sí! Las personas |
|  personnes sont comme ça.       |  mayores son así.       |
+-----------------------------------------------------------+
|  ▲ [Gramática] [Fonética] [Palabras]                      |
|  Resumen: Frase declarativa simple en presente...         |
|  Tiempo clave: Présent de l'indicatif (être)              |
|  -------------------------------------------------------  |
|  ▶   < >   1.0x                                           |
+-----------------------------------------------------------+
```

### Tooltip de palabra

```
     ,------------------------,
     |  grandes /gʁɑ̃d/        |
     |  adj. 'grandes' [📌]    |
     '------------------------'
> Mais oui ! Les [grandes]      |  ¡Pues sí! Las personas
  personnes sont comme ça.      |  mayores son así.
```

### Lector (Móvil — columnas apiladas)

```
+---------------------------------+
| < Le Petit Prince, Cap. 1       |
+---------------------------------+
| Original (FR)                   |
|---------------------------------|
|> Mais oui ! Les grandes         |
|  personnes sont comme ça.       |
+ - - - - - - - - - - - - - - - - +
| Traducción (ES)                 |
|---------------------------------|
|  ¡Pues sí! Las personas         |
|  mayores son así.               |
+---------------------------------+
|  ▲ [Gramática] [Fonética] ...   |
|  ▶   < >   1.0x                 |
+---------------------------------+
```

### Flashcards

```
+-----------------------------------------------------------+
| Flashcards (Hoy: 15 nuevas, 32 a repasar)                 |
+-----------------------------------------------------------+
|                  [ voltear ↻ ]                            |
|  +-----------------------------------------------------+  |
|  |             Les grandes personnes                   |  |
|  |                 sont comme ça.                      |  |
|  +-----------------------------------------------------+  |
|    (Difícil)          (Regular)          (Fácil)          |
|      [ 1m ]             [ 10m ]            [ 4d ]         |
+-----------------------------------------------------------+
|  [📚]  [🃏]  [📖]  [📊]                                    |
+-----------------------------------------------------------+
```

## 4. Árbol de Interacción

| Acción | Respuesta del sistema |
|---|---|
| Abre la app | Muestra P1: Biblioteca con libros y progreso |
| Toca un libro | Transición suave a P2: Lector, último capítulo leído |
| Toca una línea | Resalta línea + panel inferior se desliza con análisis |
| Toca una palabra | Tooltip flotante con IPA, traducción, botón flashcard |
| Toca 📌 en tooltip | Guarda en mazo de flashcards |
| Toca pestaña en panel | Cross-fade a Gramática / Fonética / Palabras |
| Scroll hacia abajo | Barra de herramientas se desvanece |
| Toca "voltear" en flashcards | Animación 3D de volteo |
| Toca Difícil/Regular/Fácil | Algoritmo SM-2 recalcula próximo repaso |

## 5. Sistema de Colores

| Rol | Light | Dark |
|---|---|---|
| Fondo | `#FAF8F5` Beige | `#1C1C1E` Casi negro |
| Texto | `#1F1F1F` Gris oscuro | `#EAEAEA` Gris claro |
| Acento | `#8B5E3C` Terracota | `#D4A373` Café claro |
| Tarjetas | `#FFFFFF` Blanco | `#2C2C2E` Gris oscuro |
| Gramática | `#4A7C59` Verde | `#A3D9B1` Verde menta |
| Fonética | `#B85450` Rojo teja | `#F5B8B5` Rojo pastel |
| Contraste | `#5A7C9E` Azul | `#B8D0E8` Azul cielo |

## 6. Animaciones

| Elemento | Animación | Duración | Easing |
|---|---|---|---|
| Transición de pantalla | Fade | 200ms | ease-in-out |
| Panel de análisis | slideUp | 250ms | cubic-bezier(0.2,0.8,0.2,1) |
| Tooltip palabra | fadeIn + scale | 150ms | ease-out |
| Cambio de pestaña | cross-fade | 150ms | ease |
| Hover botón | escala 0.98 | 100ms | ease |

## 7. Plan de Implementación

| Fase | Qué | Prioridad |
|---|---|---|
| **1. El Lector (MVP Core)** | Dos columnas, análisis de línea, tooltip de palabra | Ahora |
| **2. Biblioteca** | Grid, BookCard, navegación entre pantallas | Siguiente |
| **3. Flashcards** | SRS SM-2, guardar palabras, repaso | Post-MVP |
| **4. Diccionario/Progreso** | Búsqueda, estadísticas, historial | V2 |
| **5. Pulido** | Animaciones, responsive, modo oscuro, lazy loading | V2 |

---

*Diseño original generado por Gemini. Implementación por Hermes Agent.*
