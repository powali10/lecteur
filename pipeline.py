#!/usr/bin/env python3
"""
Pipeline: text → Gemini analysis → enrich with offline data → JSON universal.

Usage: uv run pipeline.py <input.json> [output.json]

Input format: { "lines": [{ "fr": "...", "es": "..." }] }
Output format: Universal JSON schema
"""

import json
import os
import subprocess
import sys
import re

# Paths
LLM_BIN = "/opt/data/home/.local/share/uv/tools/llm/bin/llm"
CONJUGATIONS_FILE = "/opt/data/lecteur/data/conjugations-fr.json"
DICTIONARY_FILE = "/opt/data/lecteur/data/dictionary-fr-es.json"

# Load offline data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def call_gemini(prompt, timeout=60):
    """Call Gemini via llm CLI."""
    result = subprocess.run(
        ["llm", "-m", "gemini", prompt],  # Gemini Flash (rápido)
        capture_output=True, text=True, timeout=timeout
    )
    out = result.stdout.strip()
    # Remove markdown code fences if present
    out = re.sub(r'^```(?:json)?\s*', '', out)
    out = re.sub(r'\s*```$', '', out)
    return out

def analyze_sentence(fr_text, es_text, idx, conjugations, dictionary):
    """Analyze one sentence with Gemini and enrich with offline data."""
    prompt = f"""Eres un lingüista experto en fonética y gramática francesa. Analiza esta frase para un estudiante hispanohablante.

FRANCÉS: {fr_text}
ESPAÑOL: {es_text}

Devuelve SOLO un objeto JSON válido. Sin markdown, sin explicación extra.

Estructura exacta:
{{
  "idx": {idx},
  "fr": "{fr_text}",
  "es": "{es_text}",
  "ipa": "/transcripción IPA completa/",
  "grammar": {{
    "summary": "Resumen gramatical de la frase (2-3 oraciones)",
    "tense_focus": {{"tense": "tiempo verbal principal", "explanation": "por qué se usa aquí"}},
    "key_rules": [
      {{"rule": "Nombre regla", "detail": "Explicación detallada"}}
    ]
  }},
  "words": [
    {{"w": "palabra", "ipa": "/ipa/", "t": "traducción", "pos": "parte de la oración", "lemma": "lema", "detail": "explicación lingüística breve"}}
  ],
  "phonetics": {{
    "features": [
      {{"feature": "tipo (liaison/elision/nasal/etc)", "text": "texto relevante", "explanation": "explicación"}}
    ]
  }},
  "contrast": "Contraste con español (1-2 oraciones)"
}}

REGLAS IMPORTANTES:
- Palabras con elisión van juntas: "j'avais", "c'est", "l'intérieur", "s'appelait", "d'un"
- Contracciones van juntas: "aux", "du", "des"
- Verbos compuestos (passé composé) van como una palabra: "j'ai vu", "ont répondu"
- El IPA debe ser preciso y completo para toda la frase
- Los lemas (lemma) deben ser la forma de diccionario (infinitivo para verbos)"""

    raw = ""
    try:
        raw = call_gemini(prompt)
        # Try to parse as JSON
        data = json.loads(raw)
        
        # Enrich with offline data
        if "words" in data:
            for word in data["words"]:
                lemma = word.get("lemma", "").lower()
                w = word.get("w", "").lower()
                
                # Enrich with dictionary
                if lemma and lemma in dictionary:
                    word["dict"] = dictionary[lemma][:3]  # Top 3 translations
                
                # Enrich with conjugations
                if lemma and lemma in conjugations:
                    word["conj"] = {
                        "infinitive": conjugations[lemma]["infinitive"],
                        "tenses": list(conjugations[lemma]["tenses"].keys()),
                    }
                    # If we have participle info, add it
                    if "participe_passé" in conjugations[lemma]:
                        word["conj"]["participe_passé"] = conjugations[lemma]["participe_passé"]
                    if "participe_présent" in conjugations[lemma]:
                        word["conj"]["participe_présent"] = conjugations[lemma]["participe_présent"]
        
        return data
    
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse error for idx {idx}: {e}")
        print(f"  Raw output (first 500 chars): {raw[:500]}")
        return {
            "idx": idx,
            "fr": fr_text,
            "es": es_text,
            "ipa": "",
            "grammar": {"summary": "", "tense_focus": {}, "key_rules": []},
            "words": [],
            "phonetics": {"features": []},
            "contrast": ""
        }
    except subprocess.TimeoutExpired:
        print(f"  WARNING: Timeout for idx {idx}")
        return {
            "idx": idx,
            "fr": fr_text,
            "es": es_text,
            "ipa": "",
            "grammar": {"summary": "", "tense_focus": {}, "key_rules": []},
            "words": [],
            "phonetics": {"features": []},
            "contrast": ""
        }

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "/opt/data/lecteur/data/le-petit-prince/ch01.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "/opt/data/lecteur/data/le-petit-prince/ch01-universal.json"
    
    print(f"Loading input: {input_path}")
    input_data = load_json(input_path)
    
    print(f"Loading offline data...")
    conjugations = load_json(CONJUGATIONS_FILE)
    dictionary = load_json(DICTIONARY_FILE)
    print(f"  Conjugations: {len(conjugations)} verbs")
    print(f"  Dictionary: {len(dictionary)} lemmas")
    
    lines = input_data.get("lines", [])
    print(f"\nProcessing {len(lines)} sentences...")
    
    results = []
    for i, line in enumerate(lines):
        fr = line.get("fr", "")
        es = line.get("es", "")
        if not fr:
            continue
        
        print(f"  [{i+1}/{len(lines)}] {fr[:50]}...")
        result = analyze_sentence(fr, es, i, conjugations, dictionary)
        results.append(result)
    
    # Build universal output
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
        "sentences": results,
    }
    
    save_json(output, output_path)
    print(f"\n✅ Pipeline complete. Saved to {output_path}")
    print(f"   {len(results)} sentences processed.")
    
    # Show stats
    total_words = sum(len(s.get("words", [])) for s in results)
    print(f"   {total_words} words analyzed.")

if __name__ == "__main__":
    main()