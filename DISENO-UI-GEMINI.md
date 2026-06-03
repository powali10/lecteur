# DISENO-UI-GEMINI.md

## Documento de Diseño de Interfaz: Lector Inteligente Lecteur

> Diseñado por Gemini (product designer)
> Fecha: 3 Junio 2026
> Inspiración: papel, tinta ferrogálica, edición literaria

---

### 1. Visión y Filosofía de Diseño

Lecteur no es una app, es una **biblioteca personal**. La experiencia debe evocar la sensación de abrir un libro de edición cuidada, con anotaciones de un erudito amigo que te explica los matices en los márgenes. Nuestro diseño se basa en tres pilares:

1. **Claridad Editorial**: La tipografía, el espaciado y el ritmo visual son los protagonistas. La interfaz es un sirviente silencioso del texto.
2. **Profundidad Accesible**: La información más compleja (morfología, fonética) está a un toque de distancia, pero nunca abruma. Adoptamos el principio de *revelación progresiva*.
3. **Calma y Foco**: Creamos un entorno digital tranquilo, libre de distracciones, que invita a la lectura prolongada y al aprendizaje profundo.

---

## A. Identidad Visual ("El Taller del Editor")

Esta paleta evoca materiales nobles: papel verjurado, tinta ferrogálica, y el subrayado sutil de un lápiz rojo de editor.

### Paleta de Colores

```css
:root {
  --color-papel:      #FAF8F5; /* Un blanco roto, cálido y amable con la vista */
  --color-tinta:      #1A1A1A; /* Un negro suave, casi carbón, para el texto principal */
  --color-tinta-sec:  #6B6B6B; /* Gris medio para texto secundario, traducciones, metadatos */
  --color-acento:     #B33939; /* Un rojo borgoña, como tinta de corrección. Para links y estados activos */
  --color-acento-bg:  #F8EAEA; /* Un fondo muy sutil para highlights, basado en el acento */
  --color-borde:      #E0DCD7; /* Un color suave para bordes y separadores */
  --color-sombra:     rgba(40, 30, 20, 0.1); /* Sombra cálida y sutil */
}
```

### Tipografía

Usamos `system-ui` por rendimiento y familiaridad, pero lo tratamos con el respeto de una tipografía de autor. La clave está en la escala, el peso y el espaciado.

- **Stack CSS**: `font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "system-ui", sans-serif;`
- **Texto Original (Source)**: `font-size: 1.1875rem (19px)`; `line-height: 1.7`; `color: var(--color-tinta);`
- **Traducción**: `font-size: 1rem (16px)`; `line-height: 1.6`; `color: var(--color-tinta-sec);` `font-style: italic;`
- **Títulos/UI (Breadcrumb)**: `font-size: 0.875rem (14px)`; `font-weight: 500`; `color: var(--color-tinta-sec);`
- **Panel/Tooltip (Cuerpo)**: `font-size: 1rem (16px)`; `line-height: 1.6`;
- **Panel/Tooltip (Etiquetas)**: `font-size: 0.8125rem (13px)`; `text-transform: uppercase;` `letter-spacing: 0.5px;` `font-weight: 600;` `color: var(--color-tinta-sec);`

### Escala de Espaciado

Basada en 8px:

- `--space-xs: 4px;`
- `--space-s: 8px;`
- `--space-m: 16px;`
- `--space-l: 24px;`
- `--space-xl: 32px;`
- `--space-xxl: 64px;`

### Elementos Visuales

- **Sombras**: `box-shadow: 0 4px 12px 0 var(--color-sombra);` (para tooltips y paneles)
- **Bordes**: `border: 1px solid var(--color-borde);`
- **Radio de borde**: `border-radius: 8px;` (sutilmente redondeado)

---

## B. Layout Completo (Desktop-First)

El layout se estructura con CSS Grid para máxima flexibilidad y claridad.

### Estructura Principal (`.reader-container`)

```css
.reader-container {
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 1fr min(1200px, 90vw) 1fr;
  grid-template-areas:
    "header header header"
    ".      main   ."
    "panel  panel  panel";
  min-height: 100vh;
  background-color: var(--color-papel);
}

#reader-header { grid-area: header; }
#main-content  { grid-area: main; }
#analysis-panel{ grid-area: panel; } /* Oculto por defecto */
```

### Estructura del Contenido Principal (`#main-content`)

```css
#main-content {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr; /* La columna original es más ancha */
  gap: var(--space-xxl);
  padding: var(--space-xl) 0;
}
```

**Zonas:**

1. **Header (`#reader-header`)**: Breadcrumb y controles globales. Sutil y fijo arriba.
2. **Contenido Principal (`#main-content`)**: El corazón.
   - `.source-column`: El texto original. Generoso, legible, el foco principal.
   - `.translation-column`: La traducción. Nota marginal, itálico, color claro.
3. **Panel de Análisis (`#analysis-panel`)**: "Cajón" que se desliza desde abajo. No interrumpe el flujo.

---

## C. Componentes

### 1. Línea de Lectura (`.sentence-pair`)

Cada frase es una unidad interactiva.

```html
<div class="sentence-pair" id="ch1_s1">
  <div class="source-line" lang="fr">
    <button class="play-btn">▶</button>
    <p>
      <span class="token" data-token-id="0">J'ai</span>
      <span class="token" data-token-id="1">dessiné</span>
      <!-- ... más tokens -->
    </p>
  </div>
  <div class="translation-line" lang="es">
    <p>Dibujé una serpiente boa que digería un elefante.</p>
  </div>
</div>
```

- **Estado activo**: Fondo `var(--color-acento-bg)` y panel se abre.

### 2. Tooltip de Palabra (`#word-tooltip`)

Aparece al tocar un `<span class="token">`.

```
┌─────────────────────────────────┐
│  digérait                       │
│  /di.ʒe.ʁɛ/   [🔊]             │
│                                 │
│  VERBO • 3ª SING • IMPARFAIT    │
│  → "digería"                    │
│                                 │
│  [📘 Ver conjugación completa]   │
│  [📌 Guardar a flashcards]       │
│  [📖 Ver en diccionario]         │
└─────────────────────────────────┘
```

- **Contenedor**: `position: absolute`, fondo papel, sombra, `max-width: 300px`, padding `--space-m`
- **Palabra**: `font-size: 1.25rem`, `font-weight: 600`, color tinta
- **IPA+Audio**: color tinta-sec, botón 🔊 inline
- **Etiquetas**: badges con padding y border-radius
- **Traducción**: directa, clara
- **Acciones**: links con iconos, color acento

### 3. Panel de Análisis (`#analysis-panel`)

El cerebro pedagógico. Se desliza desde abajo.

- **Contenedor**: `position: fixed; bottom: 0; height: 40vh;`, fondo papel, `border-top`, sombra
- **Transición**: `transform: translateY(100%)` → `translateY(0)`, `transition: 0.4s ease-in-out`
- **Header**: Frase activa + botón cerrar [X]
- **Pestañas**: `📖 Gramática`, `🔤 Fonética`, `📝 Palabras`
- **Scroll interno**: `overflow-y: auto` para contenido largo

---

## D. Pedagogía: El Caso "digérait"

Cuando el usuario toca la frase y va a **📖 Gramática**:

---

**TÉRMINO ANALIZADO: `digérait`**

---

**1. Identificación**

- **Verbo**: *digérer* (digerir)
- **Forma**: 3ª persona del singular
- **Tiempo Verbal**: **Imparfait de l'indicatif** (Pretérito Imperfecto de Indicativo)

**2. ¿Qué significa "Imparfait" aquí?**

El *Imparfait* describe una **acción en progreso o habitual en el pasado**, sin un principio o fin definidos. Es el tiempo de los fondos, las descripciones y las rutinas.

- **En la frase**: La digestión del elefante era un proceso continuo, el "fondo" de la historia. No es una acción puntual que terminó.
- **Contraste clave**: No se usa *Passé Composé* (*a digéré*) porque eso implicaría que la digestión fue una acción única y completada.

**3. Formación del Imparfait**

Se forma tomando la raíz de la 1ª persona del plural (*nous*) del presente y añadiendo las terminaciones `-ais, -ais, -ait, -ions, -iez, -aient`.

- Ejemplo con *digérer*:
  1. Presente: `nous digérons`
  2. Raíz: `digér-`
  3. Terminación (3ª sing): `+ ait` → **`digérait`**

**4. Recursos**

- [📘 Ver conjugación completa de `digérer`] → Abre modal/tabla de conjugación
- [🧠 Leer artículo: Imparfait vs. Passé Composé] → Regla gramatical completa
- [✨ Explorar verbos similares (-érer)] → lista: *considérer, espérer, posséder*

---

## E. Controles de Audio

- **Botón Play**: Al inicio de cada línea original. SVG simple.
- **Resaltado "Karaoke"**: Token activo → clase `.playing`, `background-color: var(--color-acento-bg)`, `transition: 0.1s`
- **Velocidad**: Barra superior. `[0.5x] [0.75x] [1x] [1.25x] [1.5x]`. Activo con fondo acento.
- **Auto-avance**: Toggle en header, al terminar una frase pasa a la siguiente.

---

## F. Modo Inmersión

- **Ocultar traducción**: `.translation-column` → `opacity: 0.1`, transición 0.3s. Al tocar la frase, vuelve a 1.
- **Distancia de seguridad**: `border-right: 1px dashed var(--color-borde)` en columna original.

---

## G. Modo Oscuro

```css
[data-theme="dark"] {
  --color-papel:      #1A1A1C; /* Fondo carbón */
  --color-tinta:      #E8E6E3; /* Texto cálido claro */
  --color-tinta-sec:  #9A9A9A;
  --color-acento:     #E06B6B; /* Borgoña más claro */
  --color-acento-bg:  #2A1F1F;
  --color-borde:      #2C2C2E;
  --color-sombra:     rgba(0, 0, 0, 0.3);
}
```

---

## H. Responsive

### Tablet (768px - 1024px)

```css
@media (max-width: 1024px) {
  #main-content {
    gap: var(--space-l);
  }
}
```

### Móvil (< 768px)

```css
@media (max-width: 768px) {
  #main-content {
    grid-template-columns: 1fr;
  }
  .sentence-pair {
    display: flex;
    flex-direction: column;
    gap: var(--space-s);
  }
  .translation-column { font-style: italic; }
}
```

- **Panel en móvil**: Al tocar frase: la frase queda sticky arriba, panel cubre 40% inferior, resto del contenido detrás.
- **Tap targets**: mínimo 44px.
- **Gestos**: swipe left/right entre capítulos.

---

## I. Diagrama de Flujo

| Acción del usuario | Respuesta del sistema |
|---|---|
| Carga la página | Muestra skeleton, carga JSON, renderiza libro |
| Se desplaza | Scroll suave, header fijo |
| Toca un token (`<span class="token">`) | Cierra tooltip anterior, renderiza y muestra tooltip junto al token |
| Toca fuera del tooltip | Cierra tooltip con animación |
| Toca una frase (no token) | Cierra tooltips, marca frase activa, desliza panel de análisis, muestra Gramática/Fonética/Palabras |
| Toca [X] en panel | Desliza panel abajo, quita estado activo |
| Toca [Ver conjugación] en tooltip | Cierra tooltip, activa frase, abre panel en pestaña Gramática, scrollea al verbo específico |
| Toca botón Play | Reproduce audio frase, resalta tokens en secuencia |
| Cambia velocidad | Guarda en localStorage, aplica a `speechSynthesis` |

---

## J. Estados

| Estado | Visual |
|---|---|
| **Loading** | Skeleton: barras grises animadas donde irá el texto |
| **Empty** | Mensaje: "No hay contenido cargado. Selecciona un libro." |
| **Error** | Banner sutil: "Error al cargar el capítulo. Intenta de nuevo." con botón de reintento |
| **Activo (frase)** | Fondo `--color-acento-bg`, panel visible |
| **Reproduciendo** | Token activo con fondo `--color-acento-bg` + transición |
| **Tooltip visible** | Animación fade+slide, sombra |

---

*Diseño original generado por Gemini. Implementación por Hermes Agent.*