#!/usr/bin/env python3
"""
Pipeline batch: send ALL sentences to Gemini at once for efficiency.
"""

import json, os, subprocess, sys, re

LLM = "/opt/data/home/.local/share/uv/tools/llm/bin/llm"
CONJ = "/opt/data/lecteur/data/conjugations-fr.json"
DICT = "/opt/data/lecteur/data/dictionary-fr-es.json"

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    in_path = sys.argv[1] if len(sys.argv) > 1 else "/opt/data/lecteur/data/le-petit-prince/ch01.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/opt/data/lecteur/data/le-petit-prince/ch01-universal.json"
    
    print(f"Loading: {in_path}")
    input_data = load_json(in_path)
    lines = input_data.get("lines", [])
    
    print(f"Loading offline data: conjugations + dictionary")
    conjugations = load_json(CONJ)
    dictionary = load_json(DICT)
    
    # Build prompt with ALL sentences
    prompt_parts = [
        "Eres un lingüista experto. Analiza CADA frase en francés para un estudiante hispanohablante.",
        "Devuelve SOLO un array JSON válido. Sin markdown, sin explicación.",
        "",
        "FRASES:"
    ]
    for i, line in enumerate(lines):
        prompt_parts.append(f"{i}: FR: {line['fr']}")
        prompt_parts.append(f"   ES: {line['es']}")
    
    prompt_parts.append("")
    prompt_parts.append("""ESTRUCTURA de cada elemento del array:
{
  "idx": N,
  "fr": "texto original",
  "es": "traducción",
  "ipa": "/ipa completo/",
  "grammar": {
    "summary": "resumen gramatical (2-3 oraciones)",
    "tense_focus": {"tense": "tiempo principal", "explanation": "por qué se usa"},
    "key_rules": [{"rule": "nombre", "detail": "explicación"}]
  },
  "words": [
    {"w": "palabra", "ipa": "/ipa/", "t": "traducción", "pos": "parte oración", "lemma": "lema", "detail": "explicación breve"}
  ],
  "phonetics": {
    "features": [{"feature": "liaison/elision/nasal/etc", "text": "texto", "explanation": "explicación"}]
  },
  "contrast": "contraste con español"
}

REGLAS:
- Elisiones juntas: "j'avais", "c'est", "l'intérieur", "d'un"
- Contracciones juntas: "aux", "du", "des"  
- Passé composé como una palabra: "j'ai vu"
- Lemas en infinitivo para verbos""")
    
    prompt = "\n".join(prompt_parts)
    print(f"\nSending {len(lines)} sentences to Gemini Flash...")
    print(f"Prompt length: {len(prompt)} chars")
    
    result = subprocess.run(
        [LLM, "-m", "gemini", prompt],
        capture_output=True, text=True, timeout=300
    )
    
    raw = result.stdout.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw (first 1000): {raw[:1000]}")
        return
    
    # Enrich with offline data
    for sentence in data:
        if "words" in sentence:
            for word in sentence["words"]:
                lemma = word.get("lemma", "").lower()
                if lemma in dictionary:
                    word["dict"] = dictionary[lemma][:3]
                if lemma in conjugations:
                    c = conjugations[lemma]
                    word["conj_ref"] = lemma
                    if "participe_passé" in c:
                        word["part_passé"] = c["participe_passé"]
    
    output = {
        "book_metadata": {
            "title": input_data.get("book", "Unknown"),
            "chapter": input_data.get("chapter", 1),
            "chapter_title": input_data.get("title", ""),
            "source_language": "fr",
            "target_language": "es",
            "schema_version": "1.0",
            "processing_date": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip(),
        },
        "sentences": data,
        "_offline_data": {
            "conjugations_count": len(conjugations),
            "dictionary_count": len(dictionary),
        },
        "metadata": {
            "processed_with": "gemini-flash",
            "conjugations_file": "conjugations-fr.json",
            "dictionary_file": "dictionary-fr-es.json",
        }
    }
    
    save_json(output, out_path)
    total_words = sum(len(s.get("words", [])) for s in data)
    print(f"\n✅ Done. {len(data)} sentences, {total_words} words.")
    print(f"   Saved: {out_path}")
    print(f"   Conjugations referenced: {sum(1 for s in data for w in s.get('words', []) if 'conj_ref' in w)}")
    print(f"   Dictionary references: {sum(1 for s in data for w in s.get('words', []) if 'dict' in w)}")

if __name__ == "__main__":
    main()