from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from step02_read_and_chunk import DEFAULT_SOURCE_DIR, REPO_ROOT
from step04_semantic_retrieval import DEFAULT_MODEL, build_chunk_records, load_embedding_model
from step04b_semantic_retrieval_content_filter import classify_record


INDEX_DIR = REPO_ROOT / "rag" / "data" / "vector_index"
EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npy"
METADATA_PATH = INDEX_DIR / "metadata.json"
MANIFEST_PATH = INDEX_DIR / "manifest.json"


def build_retrievable_records() -> list[dict]:
    records = build_chunk_records(DEFAULT_SOURCE_DIR)
    candidates: list[dict] = []

    for record in records:
        role, reason = classify_record(record)
        if role == "content":
            candidates.append({**record, "role": role, "reason": reason})

    return candidates


def main() -> None:
    print("RAG LAB — Paso 05A: construir índice vectorial persistente mínimo")
    print(f"Carpeta fuente: {DEFAULT_SOURCE_DIR}")
    print(f"Carpeta índice: {INDEX_DIR}\n")
    print("Objetivo de aprendizaje:")
    print("- generar embeddings una vez para los chunks recuperables")
    print("- guardar vectores + metadata de forma persistente")
    print("- separar el momento de INDEXACIÓN del momento de CONSULTA")
    print("- todavía NO usamos una base vectorial especializada\n")

    records = build_retrievable_records()
    if not records:
        print("No se encontraron chunks recuperables para indexar.")
        return

    model = load_embedding_model(DEFAULT_MODEL)
    texts = [record["searchable_text"] for record in records]
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_PATH, embeddings)

    metadata = [
        {
            "document": record["document"],
            "chunk": record["chunk"],
            "heading": record["heading"],
            "content": record["content"],
            "searchable_text": record["searchable_text"],
        }
        for record in records
    ]
    METADATA_PATH.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    manifest = {
        "model": DEFAULT_MODEL,
        "chunks": len(records),
        "dimensions": int(embeddings.shape[1]),
        "normalized_embeddings": True,
        "source_directory": str(DEFAULT_SOURCE_DIR),
        "embeddings_file": EMBEDDINGS_PATH.name,
        "metadata_file": METADATA_PATH.name,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ÍNDICE CREADO")
    print(f"- chunks indexados: {len(records)}")
    print(f"- dimensiones: {embeddings.shape[1]}")
    print(f"- embeddings: {EMBEDDINGS_PATH}")
    print(f"- metadata:   {METADATA_PATH}")
    print(f"- manifest:   {MANIFEST_PATH}\n")
    print("Idea clave:")
    print("Los embeddings de los documentos ya no desaparecen al terminar el proceso.")
    print("En la consulta siguiente cargaremos este índice y solo generaremos el embedding de la pregunta.")


if __name__ == "__main__":
    main()
