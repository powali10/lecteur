# 📖 LECTEUR — Plan de Negocio y Especificación de Producto

> **Versión:** 1.0
> **Fecha:** 3 Junio 2026
> **Autor:** Gemini (consultor de producto) + Hermes (ingeniería)

---

## 1. Resumen Ejecutivo

**Lecteur** es una plataforma web open-source de inmersión lingüística que permite aprender cualquier idioma **leyendo literatura real**. El usuario abre un ePub (o selecciona uno de la biblioteca) y la plataforma provee en una sola pantalla:

- 📖 **Lectura lado a lado** (original + traducción)
- 📝 **Gramática** por frase — no solo definiciones, sino estructura completa
- 🗣️ **Pronunciación** — IPA + fonética explicada + audio TTS
- 🔤 **Partes de la oración** — cada palabra etiquetada
- 📚 **Referencias** — reglas gramaticales, conjugaciones, excepciones
- 🃏 **Flashcards** — generación automática con repetición espaciada (SRS)
- 💬 **Traducción** — palabra, frase, contexto

**Comparación con el mercado:**

| | LingQ | Beelinguapp | ReadLang | **Lecteur** |
|---|---|---|---|---|
| Contenido real | ✅ Sí | ✅ Sí | ✅ Sí | **✅ Sí** |
| Gramática detallada | ❌ No | ❌ No | ❌ No | **✅ Sí** |
| IPA / Fonética | ❌ No | ❌ No | ❌ No | **✅ Sí** |
| Partes de la oración | ❌ No | ❌ No | ❌ No | **✅ Sí** |
| Flashcards SRS | ❌ No | ❌ No | ❌ Limitado | **✅ Sí** |
| Audio nativo TTS | ✅ | ✅ | ✅ | **✅ Edge TTS** |
| ePub propio | ❌ | ❌ | ❌ | **✅ Sí** |
| Open-source | ❌ | ❌ | ❌ | **✅ Sí** |
| Gratuito | ❌ $14/mes | ❌ $5/mes | ❌ $7/mes | **✅ Sí** |
| IA explicativa | ❌ No | ❌ No | ❌ No | **✅ Gemini** |

**Diferenciador clave:** No es solo un lector. Es un *tutor de idiomas que lee contigo*.

---

## 2. Mercado

### 2.1 Tamaño

- **Mercado global de aprendizaje de idiomas:** ~$80B USD (2026)
- **Mercado de apps:** ~$15B USD
- **Crecimiento:** ~15% anual
- **Segmento "inmersión lectora":** ~$500M (LingQ, Beelinguapp, ReadLang)

### 2.2 Competidores

| Producto | Fortaleza | Debilidad | Oportunidad para Lecteur |
|---|---|---|---|
| **LingQ** | +20M usuarios, biblioteca enorme | Caro ($14/mes), sin gramática real, UI anticuada | Ser moderno, gratuito, con IA |
| **Beelinguapp** | Diseño amigable, karaoke | Contenido limitado, solo 2 columnas | Profundidad analítica |
| **Satori Reader** | Calidad literaria japonesa | Solo japonés, caro ($11/mes) | Multi-idioma |
| **ReadLang** | Buen extractor | Sin app, sin SRS, feo | Diseño + experiencia completa |
| **Duolingo** | Gamificación masiva | No lee literatura real | Complemento natural |

### 2.3 Usuario target

**Primario** — Aprendices de nivel intermedio (A2-B2) que:
- Ya saben lo básico del idioma
- Quieren consumir contenido real
- Están frustrados con apps que solo enseñan "el gato está en la mesa"
- Quieren *entender*, no solo traducir
- Están dispuestos a leer literatura real con ayuda

**Secundario** — Políglotas, estudiantes de literatura, autodidactas avanzados

---

## 3. Modelo de Negocio

### 3.1 Estrategia: Open-source + Freemium Ético

| Capa | Precio | Qué incluye |
|---|---|---|
| **Gratis** | $0 | 3 libros simultáneos, lectura, gramática básica, flashcards limitados |
| **Suscripción** | $5/mes | Libros ilimitados, gramática avanzada, IPA explicado, flashcards ilimitados, audio descargable |
| **Patrocinador** | $10/mes | Todo lo anterior + prioridad en features, tu nombre en el repo, acceso beta |
| **Enterprise** | $50/mes | Biblioteca corporativa (escuelas, universidades), analytics, custom branding |

Pero el **core es y será open-source**. Cualquiera puede:
- Clonar el repo y correrlo gratis toda la vida
- Contribuir con traducciones, análisis gramatical, libros
- La suscripción es *para que no tengas que hostearlo tú*

### 3.2 Canales de distribución

1. **GitHub** — open-source discovery, dev community
2. **GitHub Pages** — demo funcional inmediata
3. **Product Hunt** — lanzamiento
4. **Hacker News** — "Show HN: an open-source LingQ with real AI grammar"
5. **Reddit** — r/languagelearning, r/Anki, r/French, r/Spanish
6. **YouTube** — demos, comparativas con LingQ
7. **Escuelas** — profesores de idiomas buscando herramientas gratis

### 3.3 Métricas clave (KPIs)

| Métrica | Meta 6 meses | Meta 12 meses |
|---|---|---|
| Usuarios activos semanales | 5,000 | 50,000 |
| Libros leídos (sesiones) | 50,000 | 500,000 |
| Suscriptores de pago | 200 | 2,000 |
| MRR | $1,000/mes | $10,000/mes |
| Pares de idiomas | 5 | 20+ |

---

## 4. Especificación de Producto

### 4.1 Pantalla principal: El Lector

```
┌─────────────────────────────────────────────────────────┐
│  [📚 Biblioteca]  [📝 Gramática]  [🗣️ Fonética]  [🃏 Flashcards] │ ← Nav
├─────────────────────────────────────────────────────────┤
│  Le Petit Prince — Chapitre 1          [⚙️] [⭐] [↕️]   │ ← Book bar
├────────────────────────┬────────────────────────────────┤
│                        │                                │
│  LORSQUE j'avais six   │  CUANDO yo tenía seis          │
│  ans j'ai vu, une      │  años vi, una vez,             │
│  fois, une magnifique  │  una magnífica                 │
│  image, dans un livre  │  imagen, en un libro           │
│  sur la Forêt Vierge   │  sobre la Selva Virgen         │
│  qui s'appelait        │  que se llamaba                │
│  "Histoires Vécues".   │  "Historias Vividas".          │
│                        │                                │
│  Ça représentait un    │  Representaba una              │
│  serpent boa qui       │  serpiente boa que             │
│  avalait un fauve.     │  tragaba una fiera.            │
│                        │                                │
│  ①①①①①①①①①①①①①①①①①①①│  ①①①①①①①①①①①①①①①①①①①│
│  ▸ Audio playing...                                    │
│                        │                                │
│  [← Anterior]          │          [Siguiente →]         │
├────────────────────────┴────────────────────────────────┤
│  [📖] [⚡] [🔄] [▶️] [🔊] [⏪] ⏩ [🔤] [i] [⏱️]  [1.0x] │ ← Controls
└─────────────────────────────────────────────────────────┘
```

### 4.2 Modos de interacción

#### 📖 Lectura (default)
- Dos columnas: original | traducción
- La línea activa se resalta en ambas columnas
- Al hacer clic en una **palabra**: se abre panel inferior con:
  - Traducción
  - Parte de la oración (sustantivo m., verbo 3ra pers., etc.)
  - Transcripción IPA
  - Enlace a regla gramatical relevante
- Al hacer clic en una **frase**: se abre panel completo de gramática

#### 📝 Gramática (panel expandido al hacer clic en frase)
```
┌─────────────────────────────────────────────────────┐
│  📝 Análisis gramatical                              │
│  ─────────────────────────────────────────────────   │
│                                                      │
│  "Lorsque j'avais six ans"                           │
│                                                      │
│  [Estructura]                                        │
│  Lorsque  →  conjunción temporal ("cuando")          │
│  j'       →  pronombre sujeto "je" (elidido)         │
│  avais    →  verbe avoir, imparfait, 1ère pers.      │
│              singulier                                │
│  six      →  adjectif numéral                        │
│  ans      →  nom masculin pluriel                    │
│                                                      │
│  [Tiempo verbal: Imparfait]                          │
│  Uso: acción habitual o descripción en el pasado     │
│        → "yo tenía" (no "yo tuve")                   │
│  Formación: radical présent 1ère pers. pl. + -ais    │
│        → nous avons → j'avais                        │
│  Contraste: Passé composé ≠ Imparfait                │
│        → "j'ai eu" (evento puntual)                  │
│        → "j'avais" (estado continuo)                 │
│                                                      │
│  [Elisión: j']                                       │
│  Regla: "je" → "j'" ante vocal o 'h' muda            │
│        → j'ai, j'aime, j'avais                       │
│        → je suis, je veux, je parle                  │
│                                                      │
│  [Traducción literal]                                │
│  "Cuando yo tenía seis años"                         │
│                                                      │
│  [Práctica]                                          │
│  ▸ Crear flashcard                                   │
│  ▸ Mostrar 3 ejemplos similares                      │
│  ▸ Ejercicio: conjuga "avoir" en imparfait           │
└─────────────────────────────────────────────────────┘
```

#### 🗣️ Fonética / Pronunciación
```
┌─────────────────────────────────────────────────────┐
│  🗣️ Pronunciación                                    │
│  ─────────────────────────────────────────────────   │
│                                                      │
│  "Lorsque j'avais six ans"                           │
│                                                      │
│  [IPA]                                               │
│  /lɔʁskə ʒavɛ siz‿ɑ̃/                                │
│                                                      │
│  [Palabra por palabra]                               │
│  Lorsque   →  /lɔʁskə/   → "lorsk" (e muda)         │
│  j'avais   →  /ʒavɛ/     → "javé"                    │
│  six       →  /sis/      → [siz] por liaison         │
│  ans       →  /ɑ̃/        → nasal "on"                │
│                                                      │
│  [Liaison]                                           │
│  six_ans → /siz‿ɑ̃/                                  │
│  Regla: "x" se pronuncia /z/ antes de vocal          │
│        → six_ans, dix_ans, deux_amis                 │
│        → six_mois (sin liaison, /si mwa/)            │
│                                                      │
│  [E muet]                                            │
│  Lorsque → /lɔʁskə/ → la "e" final NO se pronuncia  │
│  Regla general: e final átona se omite               │
│        → "je" → /ʒ/, "le" → /l/                     │
│                                                      │
│  [Audio]                                             │
│  ▸ Normal  ▸ Lento (0.5x)  ▸ Sílabas                │
│  ▸ Descargar MP3                                     │
│                                                      │
│  [Diferencias con español]                           │
│  La "r" francesa es uvular /ʁ/, no alveolar /r/      │
│  Las vocales nasales /ɑ̃/, /ɛ̃/, /ɔ̃/, /œ̃/ no existen │
│  en español                                          │
└─────────────────────────────────────────────────────┘
```

#### 🃏 Flashcards (SRS)
```
┌─────────────────────────────────────────────────────┐
│  🃏 Flashcards                                       │
│  ─────────────────────────────────────────────────   │
│                                                      │
│  24 pendientes │ 15 hoy │ 8 vencidas                 │
│                                                      │
│  [Frente]                                            │
│  ┌────────────────────────────────────────────────┐ │
│  │                                                │ │
│  │        avais                                    │ │
│  │        ───────                                 │ │
│  │        "I had" (imperfect)                     │ │
│  │                                                │ │
│  │  ✨ Consejo: forma parte de "j'avais"          │ │
│  │     usado en contexto:                         │ │
│  │     "Lorsque j'avais six ans..."               │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  [Reverso]                                           │
│  ┌────────────────────────────────────────────────┐ │
│  │  avoir — imparfait, 1ère pers. sing.           │ │
│  │  /avɛ/                                         │ │
│  │                                                │ │
│  │  Radical: (nous) av- + -ais                    │ │
│  │  Uso: descripción en pasado                    │ │
│  │  Contraste: "j'eus" (passé simple, literario)  │ │
│  │                                                │ │
│  │  🔗 Ver conjugación completa de "avoir"        │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  [🔴 Difícil]  [🟡 Regular]  [🟢 Fácil]              │
│  Revisión próxima: 10 min / 1 día / 4 días          │
└─────────────────────────────────────────────────────┘
```

### 4.3 Funcionalidades clave

| Funcionalidad | MVP (Fase 1) | V2 | V3 |
|---|---|---|---|
| Lector 2 columnas | ✅ | ✅ | ✅ |
| Cargar ePubs propios | ✅ | ✅ | ✅ |
| Traducción palabra | ✅ | ✅ | ✅ |
| Traducción frase | ✅ | ✅ | ✅ |
| Audio TTS (línea por línea) | ✅ (SpeechSynthesis) | ✅ (Edge TTS) | ✅ (voces nativas reales) |
| Partes de la oración | ❌ | ✅ | ✅ |
| IPA / Fonética | ❌ | ✅ | ✅ |
| Gramática detallada por frase | ❌ | ✅ | ✅ |
| Explicación de reglas fonéticas | ❌ | ❌ | ✅ |
| Flashcards SRS | ❌ | ❌ | ✅ |
| Anki export | ❌ | ❌ | ✅ |
| Multi-idioma (>5) | ❌ | ✅ | ✅ |
| Progreso / estadísticas | ❌ | ❌ | ✅ |
| Audio lento / sílabas | ❌ | ❌ | ✅ |
| Ejercicios generados por IA | ❌ | ❌ | ✅ |
| Comunidad / contribuciones | ❌ | ❌ | ✅ |
| API para desarrolladores | ❌ | ❌ | ✅ |

### 4.4 Stack técnico

| Capa | Tecnología | Razón |
|---|---|---|
| **Frontend** | HTML + CSS + JS vanilla | Sin dependencias, funciona en GitHub Pages |
| **Parser ePubs** | JS (epub.js) | Lado cliente, sin servidor |
| **Traducción** | Gemini API (gratis) | Mejor calidad, contexto completo |
| **Gramática** | Gemini API | Análisis gramatical completo por frase |
| **IPA / Fonética** | Gemini API + reglas programáticas | Generado por IA, verificado por reglas |
| **Audio** | Edge TTS / Web Speech API | Gratuito, sin API key |
| **SRS Flashcards** | Algoritmo SM-2 (Anki) | Estándar de la industria, open-source |
| **Almacenamiento** | LocalStorage + IndexedDB | Sin servidor, datos del usuario |
| **Hosting** | GitHub Pages | Gratuito, CDN global |
| **EPUB source** | Project Gutenberg, Wikisource, ePub propio | Contenido legal y gratuito |

### 4.5 Procesos clave

#### Carga de ePub
```
1. Usuario sube ePub (o selecciona de biblioteca)
2. Parser extrae capítulos y párrafos
3. IA divide en frases y alinea original ↔ traducción
4. IA genera: POS tags, IPA, gramática, reglas fonéticas
5. Todo se guarda en IndexedDB (offline-ready)
6. Usuario comienza a leer
```

#### Generación de audio
```
1. Por cada frase, se genera audio con Edge TTS
2. Se cachea en IndexedDB / Cache API
3. Se sincroniza frase ↔ audio por duración estimada
4. Modo lento: 0.5x manteniendo tono
```

#### Sistema de flashcards
```
1. Cada palabra/frase que el usuario consulta → candidato a flashcard
2. Usuario puede crear flashcards manualmente
3. Algoritmo SM-2 decide próxima revisión
4. Repaso diario (push notification opcional)
```

---

## 5. Roadmap

### Fase 0 — Demo (YA ESTÁ) 🎉
- [x] Le Petit Prince capítulo 1
- [x] Lector 2 columnas
- [x] TTS por línea
- [x] Diccionario por palabra
- [x] Navegación por teclado
- [x] Modo oscuro/claro

### Fase 1 — MVP completo (1-2 semanas)
- [ ] Carga de ePubs reales (epub.js)
- [ ] Biblioteca con múltiples libros
- [ ] Traducción automática con Gemini
- [ ] Audio Edge TTS (voces nativas)
- [ ] Sincronización texto ↔ audio por frase
- [ ] Alineación automática FR↔ES con Gemini
- [ ] Más capítulos de Le Petit Prince

### Fase 2 — Gramática y fonética (3-4 semanas)
- [ ] POS tagging por palabra
- [ ] Análisis gramatical por frase (Gemini)
- [ ] Transcripción IPA
- [ ] Explicación de liaison, e muet, nasales
- [ ] Audio lento (0.5x)
- [ ] Panel de gramática expandible
- [ ] Segundo idioma: 🇵🇹 portugués

### Fase 3 — Aprendizaje (2-3 semanas)
- [ ] Flashcards SRS (SM-2)
- [ ] Flashcards automáticos de palabras consultadas
- [ ] Estadísticas de lectura
- [ ] Export a Anki
- [ ] Tercer idioma: 🇩🇪 alemán

### Fase 4 — Producto (1 mes)
- [ ] Multi-idioma: 10+ pares
- [ ] Biblioteca comunitaria (PRs con libros alineados)
- [ ] Hosted version con suscripción
- [ ] Landing page
- [ ] Analytics
- [ ] Más fuentes: Project Gutenberg, Wikisource

### Fase 5 — Escala (2-3 meses)
- [ ] App PWA (offline completo)
- [ ] API pública
- [ ] Plugins de idioma (comunidad)
- [ ] Gemini fine-tuned para gramática
- [ ] App mobile (Tauri / Capacitor)

---

## 6. Estrategia de Contenido

### Libros iniciales por idioma

**Francés → Español**
| Libro | Autor | Disponibilidad |
|---|---|---|
| Le Petit Prince | Saint-Exupéry | ✅ PD |
| L'Étranger | Camus | ✅ PD |
| La Pesanteur et la Grâce | Simone Weil | ✅ PD (1947) |
| Les Misérables (extractos) | Hugo | ✅ PD |
| Le Spleen de Paris | Baudelaire | ✅ PD |

**Portugués → Español**
| Libro | Autor |
|---|---|
| O Pequeno Príncipe | Saint-Exupéry |
| Dom Casmurro | Machado de Assis |
| Vidas Secas | Graciliano Ramos |
| Capitães da Areia | Jorge Amado |

**Alemán → Español**
| Libro | Autor |
|---|---|
| Der kleine Prinz | Saint-Exupéry |
| Die Verwandlung | Kafka |
| Siddhartha | Hesse |
| Der Process | Kafka |

**Inglés → Español**
| Libro | Autor |
|---|---|
| The Little Prince | Saint-Exupéry |
| Animal Farm | Orwell |
| The Old Man and the Sea | Hemingway |
| The Great Gatsby | Fitzgerald |

---

## 7. Riesgos y mitigaciones

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Costo de API (Gemini) | Media | Alto | Caché agresivo, modelos baratos (Gemini Flash), opción BYOK |
| Calidad de traducción IA | Media | Alto | Revisión humana, comunidad, votos |
| Competidores copian | Baja | Medio | Open-source = ventaja (comunidad > producto) |
| Poco tráfico | Media | Alto | Content marketing, SEO, partnerships con profesores |
| ePubs con DRM | Alta | Bajo | Solo ePubs libres de DRM (PD, creative commons) |
| Costos de hosting | Baja | Bajo | GitHub Pages es gratis hasta ~100GB/mes |

---

## 8. Llamado a la acción

**Ahora mismo:** El demo está en https://powali10.github.io/lecteur/

**Próximo paso:** Fase 1 — carga de ePubs reales con traducción automática por Gemini.

**Pregunta para Fer:** ¿Quieres que siga yo construyendo o prefieres que le pase la especificación a Codex/Claude Code para que ejecute en paralelo?

---

> *"Apprendre une langue, ce n'est pas apprendre des mots. C'est apprendre à habiter un autre monde."*
