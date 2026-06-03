# Esquema Universal JSON para Lecteur

> Diseñado por Gemini
> Versión 1.0

---

## 1. Estructura del Libro (raíz)

```json
{
  "book_metadata": {
    "title": "Le Petit Prince",
    "author": "Antoine de Saint-Exupéry",
    "source_language": "fr",
    "target_language": "es",
    "schema_version": "1.0",
    "publication_date": "1943-04-06",
    "processing_date": "2023-10-27T10:00:00Z"
  },
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Chapitre I",
      "sentences": [ ]
    }
  ],
  "dictionary": {
    "avoir": {
      "lemma_id": "lem_fr_1",
      "pos": ["VERB"],
      "translations_es": [
        { "translation": "tener", "context": "Posesión" },
        { "translation": "haber", "context": "Verbo auxiliar" }
      ],
      "grammar_rule_ids": ["fr_auxiliary_verbs"],
      "conjugation_id": "fr_conj_avoir"
    }
  },
  "grammar_rules": { },
  "conjugation_tables": { },
  "declension_tables": { }
}
```

## 2. Frase (Sentence) — universal

Cada frase puede venir de: texto (libro/ePub), YouTube, podcast, audiolibro, o cualquier fuente con transcripción.

```json
{
  "sentence_id": "ch1_s1",
  "source_text": "J'ai dessiné un serpent boa qui digérait un éléphant.",
  "translation_es": "Dibujé una serpiente boa que digería un elefante.",
  "audio_ref": "audio/fr/ch1/s1.mp3",
  
  "media": {
    "type": "book",                  // "book" | "youtube" | "podcast" | "audiobook" | "transcript"
    "external_url": null,            // URL del video/audio original (YouTube, etc.)
    "external_id": null,             // YouTube video ID, podcast episode ID, etc.
    "timestamp": null,               // "00:01:23" — para sincronización video/audio
    "duration_sec": null,            // Duración de esta frase en segundos
    "source_title": null,            // Título del video/episodio
    "source_author": null            // Autor del canal/podcast
  },
  
  "phonetics": {
    "full_ipa": "/ʒe desine œ̃ sɛʁpɑ̃ boa ki diʒeʁɛ‿t‿œ̃n‿elefɑ̃/",
    "features": [
      { "type": "liaison", "from": "t8", "to": "t9", "ipa_bridge": "t" },
      { "type": "liaison", "from": "t9", "to": "t10", "ipa_bridge": "n" }
    ]
  },
  "tokens": [ ]
}
```

### Ejemplo: YouTube

```json
{
  "sentence_id": "yt_corbeau1",
  "source_text": "Mais le corbeau, ne se déconcerte pas.",
  "translation_es": "Pero el cuervo no se desconcierta.",
  "media": {
    "type": "youtube",
    "external_url": "https://youtube.com/watch?v=abc123",
    "external_id": "abc123",
    "timestamp": "00:03:45",
    "duration_sec": 2.1,
    "source_title": "Le Corbeau et le Renard",
    "source_author": "Français Authentique"
  },
  "audio_ref": "audio/fr/yt_abc123/s3.mp3",
  "phonetics": { "features": [...] },
  "tokens": [...]
}
```

### Ejemplo: Podcast

```json
{
  "sentence_id": "pc_ep1_s5",
  "source_text": "Je vais vous raconter une histoire incroyable.",
  "translation_es": "Voy a contarles una historia increíble.",
  "media": {
    "type": "podcast",
    "external_url": "https://open.spotify.com/episode/xyz",
    "external_id": "xyz789",
    "timestamp": "00:12:30",
    "duration_sec": 3.5,
    "source_title": "InnerFrench - Épisode 42",
    "source_author": "Hugo"
  },
  "phonetics": { "features": [...] },
  "tokens": [...]
}
```

## 3. Token (palabra)

```json
{
  "token_id": "ch1_s1_t1",
  "text": "J'",
  "lemma": "je",
  "pos": "PRON",
  "translation_es": "Yo",
  "lemma_ref": "je",
  "phonetics": { "ipa": "/ʒ/" },
  "morphology": {
    "person": "1",
    "number": "singular"
  },
  "language_specific": {
    "fr": { "elision_of": "je" },
    "ja": {
      "reading": "わたし",
      "romaji": "watashi",
      "inflection_type": "Polite (ます form)"
    },
    "zh": {
      "pinyin": "wǒ",
      "pinyin_numeric": "wo3",
      "stroke_count": 8
    },
    "ru": {
      "animacy": "inanimate",
      "verb_aspect": "perfective"
    },
    "la": {
      "vowel_quantity": "long",
      "phonetic_system": "classical"
    }
  }
}
```

## 4. Regla Gramatical

```json
{
  "rule_id": "fr_imparfait",
  "language": "fr",
  "title": "L'Imparfait",
  "explanation_es": "Tiempo verbal que describe acciones habituales, estados o descripciones en el pasado. Se usa para el 'fondo' de una narración.",
  "structure": "Radical (nous présent) + -ais, -ais, -ait, -ions, -iez, -aient",
  "examples": [
    {
      "fr": "Quand j'étais petit...",
      "es": "Cuando era pequeño..."
    }
  ],
  "exceptions": ["être es irregular: j'étais, tu étais, il était..."],
  "contrast_with_spanish": "Similar al pretérito imperfecto español, pero el francés lo usa en contextos donde el español usaría el indefinido.",
  "tags": ["pasado", "verbo", "descripción"],
  "related_rules": ["fr_passe_compose", "fr_plus_que_parfait"]
}
```

## 5. Conjugación

```json
{
  "conjugation_id": "fr_conj_avoir",
  "infinitive": "avoir",
  "language": "fr",
  "tenses": {
    "présent": {
      "je": "ai", "tu": "as", "il/elle": "a",
      "nous": "avons", "vous": "avez", "ils/elles": "ont"
    },
    "imparfait": {
      "je": "avais", "tu": "avais", "il/elle": "avait",
      "nous": "avions", "vous": "aviez", "ils/elles": "avaient"
    },
    "passé composé": {
      "auxiliary": "avoir",
      "participle": "eu"
    },
    "futur": {
      "je": "aurai", "tu": "auras", "il/elle": "aura",
      "nous": "aurons", "vous": "aurez", "ils/elles": "auront"
    },
    "conditionnel": {
      "je": "aurais", "tu": "aurais", "il/elle": "aurait",
      "nous": "aurions", "vous": "auriez", "ils/elles": "auraient"
    },
    "subjonctif": {
      "que je": "aie", "que tu": "aies", "qu'il/elle": "ait",
      "que nous": "ayons", "que vous": "ayez", "qu'ils/elles": "aient"
    }
  }
}
```

## 6. Declinación (ruso, latín)

```json
{
  "declension_id": "la_decl_rosa",
  "lemma": "rosa",
  "language": "la",
  "declension_type": "1st",
  "gender": "feminine",
  "cases": {
    "nominative": { "singular": "rosa", "plural": "rosae" },
    "genitive":   { "singular": "rosae", "plural": "rosarum" },
    "dative":     { "singular": "rosae", "plural": "rosis" },
    "accusative": { "singular": "rosam", "plural": "rosas" },
    "ablative":   { "singular": "rosa",  "plural": "rosis" },
    "vocative":   { "singular": "rosa",  "plural": "rosae" }
  }
}
```

## 7. Ejemplos por idioma

### FR — "J'ai vu un éléphant"
```json
{
  "sentence_id": "ex_fr",
  "source_text": "J'ai vu un éléphant.",
  "translation_es": "Vi un elefante.",
  "phonetics": { "full_ipa": "/ʒe vy œ̃‿n‿elefɑ̃/" },
  "tokens": [
    { "text": "J'ai", "lemma": "avoir", "pos": "AUX", "ipa": "/ʒe/",
      "morphology": {"person": "1", "tense": "présent", "mood": "indicative"},
      "language_specific": {"fr": {"elision_of": "je", "conjugation_ref": "fr_conj_avoir"}} },
    { "text": "vu", "lemma": "voir", "pos": "VERB", "ipa": "/vy/",
      "morphology": {"tense": "participe passé"},
      "language_specific": {"fr": {"conjugation_ref": "fr_conj_voir"}} },
    { "text": "un", "lemma": "un", "pos": "DET", "ipa": "/œ̃/",
      "morphology": {"gender": "masc", "number": "sing"} },
    { "text": "éléphant", "lemma": "éléphant", "pos": "NOUN", "ipa": "/elefɑ̃/",
      "morphology": {"gender": "masc", "number": "sing"} }
  ]
}
```

### ZH — "我有一只大象" (Wǒ yǒu yī zhǐ dàxiàng)
```json
{
  "sentence_id": "ex_zh",
  "source_text": "我有一只大象",
  "translation_es": "Tengo un elefante.",
  "tokens": [
    { "text": "我", "lemma": "我", "pos": "PRON", "translation_es": "yo",
      "language_specific": {"zh": {"pinyin": "wǒ", "pinyin_numeric": "wo3", "stroke_count": 7}} },
    { "text": "有", "lemma": "有", "pos": "VERB", "translation_es": "tener",
      "language_specific": {"zh": {"pinyin": "yǒu", "pinyin_numeric": "you3", "stroke_count": 6}} },
    { "text": "一只", "lemma": "一只", "pos": "NUM-CLASS", "translation_es": "un (clasificador)",
      "language_specific": {"zh": {"pinyin": "yī zhǐ", "pinyin_numeric": "yi1 zhi3"}} },
    { "text": "大象", "lemma": "大象", "pos": "NOUN", "translation_es": "elefante",
      "language_specific": {"zh": {"pinyin": "dàxiàng", "pinyin_numeric": "da4xiang4", "stroke_count": [3, 12]}} }
  ]
}
```

### JA — "象を見ました" (Zō o mimashita)
```json
{
  "sentence_id": "ex_ja",
  "source_text": "象を見ました",
  "translation_es": "Vi un elefante.",
  "tokens": [
    { "text": "象", "lemma": "象", "pos": "NOUN", "translation_es": "elefante",
      "language_specific": {"ja": {"reading": "ぞう", "romaji": "zō", "pitch_accent": "HLL"}} },
    { "text": "を", "lemma": "を", "pos": "PART", "translation_es": "(partícula de objeto)",
      "language_specific": {"ja": {"reading": "を", "romaji": "o", "particle_type": "direct_object"}} },
    { "text": "見ました", "lemma": "見る", "pos": "VERB", "translation_es": "vio (cortés)",
      "language_specific": {"ja": {"reading": "みました", "romaji": "mimashita",
        "inflection": {"base": "見る", "form": "ます past", "politeness": "formal"}}} }
  ]
}
```

### RU — "Я увидел слона" (Ya uvidel slona)
```json
{
  "sentence_id": "ex_ru",
  "source_text": "Я увидел слона",
  "translation_es": "Vi un elefante.",
  "tokens": [
    { "text": "Я", "lemma": "я", "pos": "PRON", "ipa": "/ja/",
      "morphology": {"person": "1", "number": "sing", "case": "nominative"} },
    { "text": "увидел", "lemma": "увидеть", "pos": "VERB", "ipa": "/ˈuvʲɪdʲɪl/",
      "morphology": {"person": "1", "number": "sing", "gender": "masc", "tense": "past", "aspect": "perfective"} },
    { "text": "слона", "lemma": "слон", "pos": "NOUN", "ipa": "/sɫɐˈna/",
      "morphology": {"gender": "masc", "number": "sing", "case": "accusative"} }
  ]
}
```

### LA — "Elephantem vidi" (pronunciación clásica)
```json
{
  "sentence_id": "ex_la",
  "source_text": "Elephantem vidi",
  "translation_es": "Vi un elefante.",
  "phonetics": { "full_ipa": "/eleˈpʰantem ˈwidiː/" },
  "tokens": [
    { "text": "Elephantem", "lemma": "elephas", "pos": "NOUN", "ipa": "/eleˈpʰantem/",
      "morphology": {"gender": "masc", "number": "sing", "case": "accusative"},
      "language_specific": {"la": {"declension_type": "3rd", "vowel_quantity": "mixed"}} },
    { "text": "vidi", "lemma": "video", "pos": "VERB", "ipa": "/ˈwidiː/",
      "morphology": {"person": "1", "number": "sing", "tense": "perfect", "mood": "indicative", "voice": "active"},
      "language_specific": {"la": {"conjugation_type": "2nd", "macron": "vīdī"}} }
  ]
}
```

## 8. Audio

```json
// Referencia en sentence.audio_ref
"sentence": {
  "audio_ref": "audio/fr/ch1/s1.mp3",
  // Formato: audio/{lang}/{ch}/s{sentence_num}.{ext}
  // Edge TTS genera MP3, calidad estándar
}
```

## 9. YouTube / Video / Podcast Pipeline

Cualquier fuente con transcripción sincronizada entra por el mismo pipeline:

```
yt-dlp (YouTube)  ─┐
Spotify API        ─┤  →  transcripción con timestamps  →  Gemini  →  JSON universal
Podcast RSS        ─┘                                    (mismo análisis)
```

### Herramientas por fuente

| Fuente | Extracción | Pros | Contras |
|---|---|---|---|
| YouTube | `yt-dlp --write-subs` | Gratis, funciona con casi todo | Algunos videos sin subs, rate limiting |
| YouTube (auto-subs) | `yt-dlp --write-auto-subs` | Cobertura casi total | Transcripción imperfecta |
| Podcast (RSS) | `yt-dlp` URL del episodio | Abierto, estandarizado | Varía por proveedor |
| Spotify | Spotify API / spotic | APIs documentadas | Requiere auth |
| Audiolibro + texto | Alineación manual o con Gemini | Control total | Más trabajo inicial |

### Sincronización en el lector

```json
// Cada frase con timestamp permite:
{
  "sentence_id": "yt_5",
  "media": {
    "type": "youtube",
    "external_url": "https://youtube.com/watch?v=abc123",
    "external_id": "abc123",
    "timestamp": "00:03:45",
    "duration_sec": 2.1
  }
}
```

El lector muestra:
```
┌───────────────────────────────────────┐
│  ▶ Video/audio embed                 │
│  ┌───────────────────────┐           │
│  │  YouTube iframe       │           │
│  │  reproduciendo        │           │
│  └───────────────────────┘           │
│  [📝] [🗣️] [🔤]                     │
│                                       │
│  ▶ "Mais le corbeau..."   ← activa  │
│     "ne se déconcerte pas."          │  ← timestamp 00:03:45
│     "Il prend son fromage..."        │
│     "et dit: Bonjour, mon ami!"      │
│                                       │
│  La línea activa → video salta a ese timestamp
└───────────────────────────────────────┘
```

### Ventajas de este enfoque

1. **Un solo pipeline** para libros, YouTube, podcasts, audiolibros
2. **Un solo formato** JSON universal con o sin `media.timestamp`
3. **Análisis completo** (gramática, IPA, conjugaciones) sobre cualquier contenido real
4. **Offline después del pipeline** — el video/audio ya no necesita internet

## Principios del esquema

1. **Núcleo común**: source_text, translation_es, tokens con phonetics, morphology básica
2. **Extensión por idioma**: `language_specific.{lang}` para cualquier cosa que no encaje
3. **Centralización**: dictionary, grammar_rules, conjugation_tables, declension_tables a nivel de libro
4. **Audio cacheado**: referencias a archivos MP3 por frase
5. **Offline-first**: todo autocontenido en un JSON