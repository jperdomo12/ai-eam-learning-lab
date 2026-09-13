from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

from step02_read_and_chunk import DEFAULT_SOURCE_DIR, create_chunks, discover_text_documents


DEFAULT_QUERY = "procedimiento calibracion PT-201"
TOP_K = 3
STOPWORDS = {
    "a",
    "al",
    "como",
    "con",
    "cual",
    "de",
    "del",
    "el",
    "en",
    "es",
    "la",
    "las",
    "lo",
    "los",
    "para",
    "por",
    "que",
    "se",
    "segun",
    "un",
    "una",
    "y",
}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(character for character in text if not unicodedata.combining(character))
    return text.lower()


def tokenize(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", normalize(text)))
    return {token for token in tokens if token not in STOPWORDS and len(token) > 1}


def build_chunk_records(folder: Path) -> list[dict]:
    records: list[dict] = []

    for document in discover_text_documents(folder):
        for chunk_index, chunk in enumerate(create_chunks(document), start=1):
            searchable_text = f"{chunk['heading']}\n{chunk['content']}"
            records.append(
                {
                    "document": document.name,
                    "chunk": chunk_index,
                    "heading": chunk["heading"],
                    "content": chunk["content"],
                    "tokens": tokenize(searchable_text),
                }
            )

    return records


def lexical_retrieve(records: list[dict], query: str, top_k: int = TOP_K) -> list[dict]:
    query_tokens = tokenize(query)
    ranked: list[dict] = []

    for record in records:
        matched_tokens = sorted(query_tokens & record["tokens"])
        ranked.append(
            {
                **record,
                "score": len(matched_tokens),
                "matched_tokens": matched_tokens,
            }
        )

    ranked.sort(key=lambda item: (-item["score"], item["document"], item["chunk"]))
    return ranked[:top_k]


def main() -> None:
    folder = DEFAULT_SOURCE_DIR
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY

    print("RAG LAB — Paso 03: retrieval léxico mínimo")
    print(f"Carpeta fuente: {folder}")
    print(f"Pregunta/búsqueda: {query}\n")
    print("Baseline de aprendizaje:")
    print("- compara palabras de la consulta con palabras de cada chunk")
    print("- score = cantidad de términos coincidentes")
    print("- todavía NO usamos embeddings ni comprensión semántica")
    print("- por eso sinónimos o formulaciones distintas pueden fallar\n")

    records = build_chunk_records(folder)
    results = lexical_retrieve(records, query)

    if not results or results[0]["score"] == 0:
        print("No hubo coincidencias léxicas útiles.")
        print("Esto NO significa necesariamente que la respuesta no exista; solo que esta búsqueda simple no la encontró.")
        return

    print(f"Top-{len(results)} chunks recuperados:\n")

    for position, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"#{position} | score={result['score']} | {result['document']} | chunk {result['chunk']}")
        print(f"Sección: {result['heading']}")
        print(f"Términos coincidentes: {', '.join(result['matched_tokens']) or '(ninguno)'}")
        print("-" * 80)
        print(result["content"])
        print()

    print("=" * 80)
    print("PRÓXIMA OBSERVACIÓN")
    print("Prueba después una formulación semánticamente equivalente pero con palabras diferentes,")
    print('por ejemplo: "¿Cómo ajusto el transmisor de presión?"')
    print("La comparación con embeddings mostrará por qué RAG suele necesitar búsqueda semántica.")
    print("=" * 80)


if __name__ == "__main__":
    main()
