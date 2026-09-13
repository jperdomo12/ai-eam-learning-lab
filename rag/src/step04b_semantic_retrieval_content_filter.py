from __future__ import annotations

import sys

from step04_semantic_retrieval import (
    DEFAULT_MODEL,
    TOP_K,
    build_chunk_records,
    load_embedding_model,
    semantic_rank,
)
from step02_read_and_chunk import DEFAULT_SOURCE_DIR


DEFAULT_QUERY = "¿Qué pasos debo seguir para ajustar correctamente un transmisor de presión?"


def classify_record(record: dict) -> tuple[str, str]:
    """Clasifica chunks estructurales/metadata sin alterar el chunking original."""
    if record["chunk"] == 1:
        return "structure", "título/aviso del documento"

    if record["heading"].strip().casefold() == "identificación":
        return "metadata", "identificación del activo/documento"

    return "content", "contenido recuperable"


def main() -> None:
    folder = DEFAULT_SOURCE_DIR
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else DEFAULT_QUERY

    print("RAG LAB — Paso 04b: retrieval semántico filtrando estructura/metadata")
    print(f"Carpeta fuente: {folder}")
    print(f"Pregunta/búsqueda: {query}\n")
    print("Variable controlada:")
    print("- mismo modelo de embeddings")
    print("- mismos documentos y mismo chunking")
    print("- misma consulta y mismo Top-k")
    print("- solo excluimos del ranking chunks estructurales o de identificación")
    print("- no se elimina el contenido fuente: solo cambia qué chunks compiten en retrieval\n")

    model = load_embedding_model(DEFAULT_MODEL)
    records = build_chunk_records(folder)

    classified: list[dict] = []
    excluded: list[dict] = []
    candidates: list[dict] = []

    for record in records:
        role, reason = classify_record(record)
        enriched = {**record, "role": role, "reason": reason}
        classified.append(enriched)
        if role == "content":
            candidates.append(enriched)
        else:
            excluded.append(enriched)

    print(f"Chunks totales: {len(classified)}")
    print(f"Chunks excluidos del retrieval: {len(excluded)}")
    print(f"Chunks candidatos a retrieval: {len(candidates)}\n")

    print("Excluidos del ranking semántico:")
    for record in excluded:
        print(
            f"- {record['document']} | chunk {record['chunk']} | "
            f"{record['heading']} | {record['role']} | {record['reason']}"
        )
    print()

    ranked, dimensions = semantic_rank(model, candidates, query)
    results = ranked[:TOP_K]

    print(f"Dimensiones del embedding: {dimensions}")
    print(f"Top-{len(results)} chunks de CONTENIDO por similitud semántica:\n")

    for position, result in enumerate(results, start=1):
        print("=" * 80)
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']}"
        )
        print(f"Sección: {result['heading']}")
        print("-" * 80)
        print(result["content"])
        print()

    print("=" * 80)
    print("RANKING COMPLETO — solo contenido recuperable")
    for position, result in enumerate(ranked, start=1):
        marker = " <== Top-k" if position <= TOP_K else ""
        print(
            f"#{position:02d} | {result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | "
            f"{result['heading']}{marker}"
        )

    print("=" * 80)
    print("OBSERVACIÓN")
    print("El experimento no cambia embeddings ni chunking; cambia solo el conjunto elegible para retrieval.")
    print("Así podemos observar la diferencia entre metadata/estructura y conocimiento operativo recuperable.")
    print("Todavía no usamos metadata EAM real ni filtros por asset/site; eso se estudiará más adelante.")
    print("=" * 80)


if __name__ == "__main__":
    main()
