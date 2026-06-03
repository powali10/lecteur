# PRD-CODEX-UI.md — Lecteur: Interfaz Rediseñada

## Contexto

Construir la interfaz de lectura de Lecteur desde cero. El diseño completo está en `DISENO-UI-GEMINI.md`. Este PRD traduce ese diseño a especificaciones implementables.

**Stack**: HTML5 + CSS3 + Vanilla JS. Sin dependencias. Sin framework. Sin backend. GitHub Pages.

**Repo**: powali10/lecteur
**Branch**: master (por ahora)
**Deploy**: https://powali10.github.io/lecteur/

## Archivos de referencia

- `DISENO-UI-GEMINI.md` — diseño completo (paleta, componentes, pedagogía, responsive)
- `data/ch01-universal.json` — datos de Le Petit Prince capítulo 1, procesados con el esquema universal
- `data/dictionary-fr-es.json` — 17,766 lemas FR→ES
- `data/conjugations-fr.json` — 7,016 verbos franceses conjugados
- `SCHEMA-UNIVERSAL.md` — esquema completo de datos

## Lo que hay que construir

Una sola página HTML (`index.html`) con:

### 1. Biblioteca (vista de libros al cargar)

Grid de libros disponibles. Cada libro se carga desde `data/{slug}/catalog.json` o similar. Por ahora solo uno: Le Petit Prince.

Cada BookCard muestra:
- Portada (placeholder, o emoji/libro)
- Título, autor
- Par de idiomas (FR→ES)
- Barra de progreso (si hay datos guardados en localStorage)
- Al tocar → abre el lector en ese libro

### 2. Lector (la pantalla principal)

#### Header
- Breadcrumb: "Le Petit Prince > Capítulo 1"
- Botón atrás (←) a la biblioteca
- Selector de velocidad: [0.5x] [0.75x] [1x] [1.25x] [1.5x]
- Toggle modo inmersión (oculta traducción)
- Toggle modo oscuro ( 🌙 / ☀️ )
- Progreso: "Frase 8 / 25" con barra tipo Kindle

#### Cuerpo (dos columnas)
- **Columna izquierda (1.2fr)**: Texto original en francés
- **Columna derecha (0.8fr)**: Traducción al español

Cada frase (`.sentence-pair`) contiene:
- Botón de play al inicio de la línea
- Tokens clickeables (`.token`)
- La traducción alineada

Al tocar una frase:
1. Se marca como activa (fondo `--color-acento-bg`)
2. Se desliza el panel de análisis desde abajo

#### Panel de Análisis (se desliza desde abajo, 40vh)

Tres pestañas:

**📖 Gramática**
- Para cada verbo en la frase: tiempo verbal con EXPLICACIÓN (no solo etiqueta)
- "¿Qué es el imparfait?" con formato pedagógico:
  - Definición en español
  - Cómo se forma (radical + terminaciones)
  - Contraste con español
  - Enlace "Ver conjugación completa de [verbo]"
  - Enlace "Explorar verbos similares"
- Implementar usando `getTenseExplanation()` con datos del JSON

**🔤 Fonética**
- IPA completo de la frase
- IPA de cada palabra con enlace al diccionario
- Palabras clickeables que abren tooltip

**📝 Palabras**
- Lista de vocabulario de la frase
- Cada palabra: lema, traducción, POS
- Botón "📌 Guardar" que persiste en localStorage

#### Tooltip de Palabra

Al tocar un token:

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

- Posicionado absolutamente cerca del token
- Cierra al tocar fuera
- Animación fade+slide (150ms)
- Max-width 300px, padding 16px
- Sombra, fondo papel

### 3. Audio

- SpeechSynthesis API del navegador (por ahora, Edge TTS después)
- Velocidad configurable guardada en localStorage
- Al reproducir, resaltado secuencial de tokens (clase `.playing`)
- Botón play por frase
- Auto-avance: toggle en header

### 4. Sistema de Diseño (CSS Variables)

```css
:root {
  --color-papel:      #FAF8F5;
  --color-tinta:      #1A1A1A;
  --color-tinta-sec:  #6B6B6B;
  --color-acento:     #B33939;
  --color-acento-bg:  #F8EAEA;
  --color-borde:      #E0DCD7;
  --color-sombra:     rgba(40, 30, 20, 0.1);
  --space-xs: 4px;
  --space-s: 8px;
  --space-m: 16px;
  --space-l: 24px;
  --space-xl: 32px;
  --space-xxl: 64px;
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}
```

### 5. Modo Oscuro

```css
[data-theme="dark"] {
  --color-papel:      #1A1A1C;
  --color-tinta:      #E8E6E3;
  --color-tinta-sec:  #9A9A9A;
  --color-acento:     #E06B6B;
  --color-acento-bg:  #2A1F1F;
  --color-borde:      #2C2C2E;
  --color-sombra:     rgba(0, 0, 0, 0.3);
}
```

Persistir preferencia en localStorage.

### 6. Responsive

- **Desktop** (>1024px): dos columnas lado a lado, panel 40vh
- **Tablet** (768-1024px): dos columnas con menos gap
- **Móvil** (<768px): columnas apiladas, panel sticky 40%, tap targets 44px+, gesture swipe entre capítulos

### 7. Estados

- **Loading**: skeleton con barras grises animadas
- **Empty**: mensaje "No hay contenido disponible"
- **Error**: banner con botón reintentar

## Estructura de datos (JSON)

El `data/ch01-universal.json` tiene:
```json
{
  "book_metadata": { ... },
  "chapters": [{
    "chapter_id": 1,
    "title": "Chapitre I",
    "sentences": [{
      "sentence_id": "ch01_s1",
      "source_text": "...",
      "translation_es": "...",
      "phonetics": { "full_ipa": "...", "features": [...] },
      "tokens": [{
        "text": "J'ai",
        "lemma": "avoir",
        "pos": "AUX",
        "ipa": "/ʒe/",
        "translation_es": "he",
        "morphology": { "person": "1", "tense": "présent", "mood": "indicative" },
        "conjugation_ref": "fr_conj_avoir",
        "lemma_ref": "avoir"
      }]
    }]
  }],
  "dictionary": { ... },
  "grammar_rules": { ... },
  "conjugation_tables": { ... }
}
```

## Reglas de implementación

1. **Un solo archivo**: `index.html` con HTML+CSS+JS inline (para GitHub Pages, sin build step)
2. **Sin dependencias externas**: no CDN, no frameworks, no npm
3. **Carga de datos**: fetch JSON del libro al cargar, mostrar skeleton mientras carga
4. **Sin API keys**: todo offline
5. **Pedagogía ante todo**: cada tiempo verbal debe tener explicación en español, no solo etiqueta
6. **Persistencia**: localStorage para: velocidad audio, modo oscuro, modo inmersión, flashcards, progreso de lectura
7. **Animaciones sutiles**: transiciones de 150-250ms, easing suave, nada brusco

## Proceso de construcción sugerido

1. Primero: index.html con el esqueleto HTML, CSS variables, layout grid básico y carga de datos
2. Segundo: sistema de diseño CSS completo (colores, tipografía, espaciado, responsive)
3. Tercero: carga de datos desde JSON, renderizado de líneas de lectura
4. Cuarto: interacciones (seleccionar frase, tooltip de token, panel de análisis)
5. Quinto: audio con SpeechSynthesis + resaltado de tokens
6. Sexto: localStorage (velocidad, modo oscuro, modo inmersión, flashcards, progreso)
7. Séptimo: modo oscuro completo, responsive móvil
8. Octavo: pulido (animaciones, skeleton loading, estados error/empty)

## Notas de diseño (detalles finos)

- La columna de traducción va en itálico y color secundario para sentirse como nota marginal
- El panel de análisis no es modal — no interrumpe, complementa
- El tooltip no cubre el token que lo invoca — aparece a un lado
- El header es sutil: fondo papel, altura pequeña (48px), sin sombra fuerte
- El scroll es suave con `scroll-behavior: smooth`
- Los bordes son `#E0DCD7` — apenas perceptibles
- La barra de progreso es tipo Kindle: línea delgada en la parte superior del header
- Los botones de velocidad en el header son pequeños, sin texto "Velocidad", solo el número