# PRD: Lecteur — Lector inmersivo con análisis lingüístico

> **Para implementar con Codex CLI**
> **Repo:** `powali10/lecteur` (rama: `feat/reader`)
> **Prioridad:** Alta

## 1. Resumen

Lecteur es un lector bilingüe inmersivo que permite aprender idiomas leyendo literatura real. El usuario ve dos columnas (original | traducción), toca una línea para ver análisis gramatical completo, toca una palabra para ver IPA + definición. Funciona 100% en el navegador, sin backend.

**Ya existe:** datos procesados, conjugaciones, diccionarios, pipeline Gemini.
**Hay que construir:** la interfaz de usuario.

## 2. Stack

- **HTML + CSS + JS vanilla** — sin frameworks, sin build step
- **GitHub Pages** — hosting
- **Datos en JSON estáticos** — carpeta `data/`

## 3. Archivos existentes

```
data/
├── dictionary-fr-es.json    (17K lemmas FR→ES)
├── dictionary-en-es.json    (17K lemmas EN→ES)
├── dictionary-pt-es.json    (7K lemmas PT→ES)
├── conjugations-fr.json     (7K verbos conjugados)
└── le-petit-prince/
    ├── ch01-universal.json   (capítulo procesado con análisis completo)
    └── ch01.json             (versión anterior básica)

DISENO-GEMINI.md             (diseño de interfaz por Gemini)
SCHEMA-UNIVERSAL.md          (esquema de datos)
index.html                   (versión básica actual — REEMPLAZAR)
```

## 4. Requerimientos funcionales

### 4.1 Biblioteca (pantalla inicial)

Grid de libros. Cada libro muestra: icono, título, autor, par de idiomas, barra de progreso. Al hacer clic → abre el lector.

Los datos vienen de `data/catalog.json`:
```json
{
  "books": [
    {
      "id": "le-petit-prince",
      "title": "Le Petit Prince",
      "author": "Antoine de Saint-Exupéry",
      "icon": "👑",
      "color": "#D4A373",
      "lang": "fr",
      "translation": "es",
      "description": "El principito enseña lo esencial a los ojos del corazón.",
      "chapters": [
        { "num": 1, "title": "Chapitre 1" }
      ]
    }
  ]
}
```

### 4.2 Lector (pantalla principal)

Layout:

```
┌──────────────────────────────────────────────┐
│  ← Biblioteca    Título del libro          ▶ │
├─────────────────────┬────────────────────────┤
│  ORIGINAL (FR)      │  TRADUCCIÓN (ES)       │
│                     │                        │
│  línea activa ▶     │  línea activa ▶        │
│                     │                        │
├─────────────────────┴────────────────────────┤
│  [📝 Gramática]  [🗣️ Fonética]  [🔤 Palabras] │
│  (panel deslizable con análisis)             │
└──────────────────────────────────────────────┘
```

**Columnas:**
- Dos columnas: original (FR, EN, PT) a la izquierda, traducción (ES) a la derecha
- Tipografía serif, tamaño ~1.1rem, interlineado 1.8
- Línea activa resaltada con borde izquierdo de color acento (#8B5E3C)
- La línea activa es la misma en ambas columnas
- Móvil: columnas apiladas

**Click en línea:**
- Resalta la línea
- Abre panel inferior con análisis de esa línea
- Panel tiene 3 pestañas: Gramática, Fonética, Palabras
- Animación slideUp del panel

**Click en palabra:**
- Muestra tooltip flotante con: palabra, IPA, traducción, definición corta, botón "➕ flashcard"
- Animación fadeIn

**Navegación teclado:**
- ↑ flecha arriba: línea anterior
- ↓ flecha abajo: línea siguiente
- Espacio: play/pausa audio

**Audio TTS:**
- Botón ▶ en toolbar
- Lee la línea actual en voz del idioma correspondiente (fr-FR, en-US, pt-BR)
- Al terminar, avanza a la siguiente línea automáticamente

### 4.3 Panel de análisis (tres pestañas)

#### 📝 Gramática
```
Resumen gramatical de la frase (texto explicativo)

⚡ TIEMPO VERBAL CLAVE
Imparfait & Passé Composé
Explicación de por qué se usa cada tiempo

▸ Regla 1: nombre — explicación detallada
▸ Regla 2: nombre — explicación detallada

🌎 CONTRASTE CON ESPAÑOL
Nota sobre diferencias clave
```

Datos vienen de: `sentence.grammar.summary`, `.tense_focus`, `.key_rules[]`, y `sentence.contrast` del JSON universal.

Estilos: fondo verde suave (#4A7C59) para tiempo verbal, azul (#5A7C9E) para contraste.

#### 🗣️ Fonética
```
🔊 TRANSCRIPCIÓN IPA
/lɔʁskə ʒavɛ si‿z‿ɑ̃.../

▸ Liaison: six_ans — /si‿z‿ɑ̃/. La 'x' se sonoriza /z/ ante vocal
▸ Elisión: j'avais — 'je' se contrae ante vocal
▸ Nasales: ans, dans — /ɑ̃/ no existe en español
```

Datos: `sentence.ipa` + `sentence.phonetics.features[]`.

Estilo: rojo suave (#B85450).

#### 🔤 Palabras
Tabla con columnas: Palabra | IPA | Traducción | Función

Cada fila enlaza al detalle de la palabra (tooltip al hacer clic).

### 4.4 Tooltip de palabra

Al hacer clic en cualquier palabra dentro de la columna original:

```
┌──────────────────────────┐
│  j'avais     /ʒavɛ/      │
│  → yo tenía              │
│  verbo (avoir, imparfait)│
│  [➕ Añadir flashcard]    │
└──────────────────────────┘
```

Datos: token `{w, ipa, t, pos, detail}` + diccionario offline + conjugación si aplica.

### 4.5 Diccionario offline

Los diccionarios (`dictionary-fr-es.json`, `dictionary-en-es.json`, `dictionary-pt-es.json`) se cargan en memoria al abrir un libro. Cuando el usuario hace clic en una palabra, se busca en:

1. `token.dict` (diccionario embebido del JSON del libro)
2. Si no está, en el diccionario offline completo

### 4.6 Modo oscuro/claro

Automático según preferencia del sistema. Toggle manual.

Variable `data-theme` en `<html>`.

Colores:
- Light: fondo #FAF8F5, texto #2B2825, acento #8B5E3C
- Dark: fondo #1C1C1E, texto #E8E4DE, acento #D4A373

## 5. Datos: formato JSON universal

El archivo `ch01-universal.json` tiene esta estructura (ver SCHEMA-UNIVERSAL.md):

```json
{
  "book_metadata": { "title": "...", "source_language": "fr", ... },
  "sentences": [
    {
      "idx": 0,
      "fr": "Lorsque j'avais six ans...",
      "es": "Cuando tenía seis años...",
      "ipa": "/lɔʁskə ʒavɛ.../",
      "grammar": {
        "summary": "...",
        "tense_focus": { "tense": "Imparfait & Passé Composé", "explanation": "..." },
        "key_rules": [ { "rule": "Elisión", "detail": "..." } ]
      },
      "words": [
        { "w": "Lorsque", "ipa": "/lɔʁskə/", "t": "Cuando", "pos": "conjunción", "lemma": "lorsque", "detail": "..." }
      ],
      "phonetics": {
        "features": [ { "feature": "Liaison", "text": "six ans", "ipa": "/si‿z‿ɑ̃/", "explanation": "..." } ]
      },
      "contrast": "..."
    }
  ]
}
```

Para EN y PT, los campos serían `source_text` y `translation_es` (formato universal). El índice actual usa `fr` y `es`.

**IMPORTANTE:** El `ch01-universal.json` actual usa `fr` y `es` como campos de texto. Soporta también `source_text` y `translation_es`. El lector debe funcionar con ambos formatos.

## 6. Diseño visual

Ver `DISENO-GEMINI.md` para el diseño completo de Gemini.

Resumen visual:
- Fondo beige, tarjetas blancas, esquinas 12px
- Tipografía: IBM Plex Serif para texto, Inter para UI
- Acento terracota #8B5E3C
- Animaciones sutiles: slideUp para panel, fadeIn para tooltips
- Responsive: funciona en móvil (columnas apiladas)

## 7. Tasks de implementación

### Task 1: Catálogo y biblioteca
- Crear `data/catalog.json` con la estructura de libros
- Implementar pantalla de biblioteca con grid de libros
- Navegación a lector al hacer clic

### Task 2: Lector básico
- Dos columnas con tipografía serif
- Cargar JSON universal y renderizar líneas
- Línea activa con borde izquierdo
- Navegación por teclado (↑↓)
- Audio TTS (Web Speech API) con Espacio

### Task 3: Panel de análisis
- Panel inferior deslizable con 3 pestañas
- Pestaña Gramática: resumen, tiempo verbal, reglas, contraste
- Pestaña Fonética: IPA, features
- Pestaña Palabras: tabla de palabras
- Animación slideUp/cross-fade

### Task 4: Tooltip de palabras
- Click en palabra → tooltip flotante con IPA + traducción + POS
- Botón "➕ flashcard" (funcionalidad: guarda en localStorage)
- Integración con diccionario offline

### Task 5: Modo oscuro y pulido
- Modo oscuro/claro automático + toggle
- Animaciones suaves
- Responsive (móvil: columnas apiladas)
- Cargar offline data (diccionarios, conjugaciones) al inicio

## 8. Criterios de aceptación

- [ ] Biblioteca muestra libros del catálogo
- [ ] Clic en libro abre el lector con el capítulo
- [ ] Dos columnas con texto alineado línea por línea
- [ ] Flechas ↑↓ navegan entre líneas
- [ ] Espacio reproduce audio TTS
- [ ] Clic en línea abre panel con análisis gramatical
- [ ] Panel tiene 3 pestañas funcionales
- [ ] Clic en palabra muestra tooltip con IPA
- [ ] Modo oscuro funciona
- [ ] Responsive en móvil
- [ ] Sin errores en consola
- [ ] Funciona con capítulo 1 (FR), y preparado para EN/PT

## 9. Notas para Codex

- Lee `DISENO-GEMINI.md` y `SCHEMA-UNIVERSAL.md` para contexto completo
- El `index.html` actual existe pero es una versión básica. REEMPLÁZALO completamente
- Usa `data/le-petit-prince/ch01-universal.json` para probar
- NO necesitas servidor — todo es HTML estático
- Commit en rama `feat/reader`