from __future__ import annotations

import argparse
import os
from pathlib import Path

from step02_read_and_chunk import create_chunks
from step04_semantic_retrieval import DEFAULT_MODEL, load_embedding_model, semantic_rank
from step04b_semantic_retrieval_content_filter import classify_record
from step06_build_grounded_context import build_context
from step08_generate_grounded_answer import (
    DEFAULT_GENERATION_MODEL,
    GENERATION_TOP_K,
    generate_with_ollama,
)
from step08b_generate_grounded_answer_prompt_completeness import build_completeness_prompt
from step09_resolve_maximo_doclinks import (
    ASSET_DOCLINK_OWNER_KEY,
    MAXIMO_MOCK_DIR,
    find_asset,
    load_json,
    resolve_documents,
)


DEFAULT_ASSETNUM = "PT-201"
DEFAULT_SITEID = "PLANTA1"
DEFAULT_QUERY = (
    "Estoy trabajando sobre el activo PT-201 en PLANTA1. "
    "¿Cómo debo calibrarlo según la documentación asociada al activo?"
)


def build_scoped_chunk_records(documents: list[dict]) -> list[dict]:
    """Construye chunks únicamente desde los documentos resueltos por Maximo mock."""
    records: list[dict] = []

    for document in documents:
        if not document.get("resolved_path") or not document.get("exists"):
            continue

        path = Path(document["resolved_path"])
        for chunk_index, chunk in enumerate(create_chunks(path), start=1):
            searchable_text = f"{chunk['heading']}\n{chunk['content']}"
            records.append(
                {
                    "document": path.name,
                    "maximo_document": document["document"],
                    "docinfoid": document["docinfoid"],
                    "doclinksid": document["doclinksid"],
                    "chunk": chunk_index,
                    "heading": chunk["heading"],
                    "content": chunk["content"],
                    "searchable_text": searchable_text,
                }
            )

    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Resuelve documentos desde contexto EAM simulado y ejecuta RAG "
            "solo sobre esos documentos."
        )
    )
    parser.add_argument("assetnum", nargs="?", default=DEFAULT_ASSETNUM)
    parser.add_argument("siteid", nargs="?", default=DEFAULT_SITEID)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    args = parser.parse_args()

    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_GENERATION_MODEL)

    assets = load_json(MAXIMO_MOCK_DIR / "assets.json")
    doclinks = load_json(MAXIMO_MOCK_DIR / "doclinks.json")
    docinfo = load_json(MAXIMO_MOCK_DIR / "docinfo.json")

    asset = find_asset(assets, args.assetnum, args.siteid)
    if not asset:
        raise SystemExit(
            f"Activo no encontrado: assetnum={args.assetnum}, siteid={args.siteid}"
        )

    documents = resolve_documents(asset, doclinks, docinfo)
    valid_documents = [
        document
        for document in documents
        if document.get("resolved_path") and document.get("exists")
    ]

    if not valid_documents:
        raise SystemExit("No hay documentos FILE existentes asociados al activo.")

    print("=== PASO 10: CONTEXTO EAM → DOCLINKS → RAG → LLM ===")
    print(f"ASSETNUM : {asset['assetnum']}")
    print(f"SITEID   : {asset['siteid']}")
    print(f"ASSETUID : {asset['assetuid']}")
    print(f"ASSETID  : {asset['assetid']}")
    print(f"OWNER KEY: {ASSET_DOCLINK_OWNER_KEY.upper()} (baseline site-specific)")
    print(f"Pregunta : {args.query}\n")

    print("1) DOCUMENTOS RESUELTOS POR MAXIMO MOCK")
    for index, document in enumerate(valid_documents, start=1):
        print(
            f"#{index} | {document['document']} | DOCINFOID={document['docinfoid']} | "
            f"{Path(document['resolved_path']).name}"
        )

    records = build_scoped_chunk_records(valid_documents)

    candidates: list[dict] = []
    excluded: list[dict] = []
    for record in records:
        role, reason = classify_record(record)
        enriched = {**record, "role": role, "reason": reason}
        if role == "content":
            candidates.append(enriched)
        else:
            excluded.append(enriched)

    if not candidates:
        raise SystemExit("Los documentos asociados no produjeron chunks recuperables.")

    print("\n2) ALCANCE RAG DETERMINADO POR EL CONTEXTO EAM")
    print(f"Documentos habilitados por Doclinks: {len(valid_documents)}")
    print(f"Chunks totales en esos documentos: {len(records)}")
    print(f"Chunks de contenido candidatos: {len(candidates)}")
    print(f"Chunks estructura/metadata excluidos: {len(excluded)}")
    print("Nota: en este Paso 10 los embeddings se calculan en memoria únicamente para los documentos seleccionados por Doclinks.")
    print("No se modifica el índice persistente de los Pasos 05–08; esta es una simplificación pedagógica, no una arquitectura productiva.\n")

    model = load_embedding_model(DEFAULT_MODEL)
    ranked, dimensions = semantic_rank(model, candidates, args.query)
    top_k = min(GENERATION_TOP_K, len(ranked))
    results = ranked[:top_k]

    print("3) RETRIEVAL SEMÁNTICO DENTRO DEL ALCANCE EAM")
    print(f"Modelo embeddings: {DEFAULT_MODEL}")
    print(f"Dimensiones: {dimensions}")
    print(f"Top-k efectivo: {top_k}")
    for position, result in enumerate(results, start=1):
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
        )

    context = build_context(results)
    prompt = build_completeness_prompt(args.query, context)

    print("\n4) GENERACIÓN FUNDAMENTADA")
    print("Runtime: Ollama")
    print(f"LLM: {model_name}")
    print("El LLM recibe el texto original de los chunks recuperados; no recibe los embeddings.\n")

    try:
        answer = generate_with_ollama(prompt, model_name)
    except Exception as exc:
        print(f"La generación local falló: {type(exc).__name__}: {exc}")
        print("La selección EAM y el retrieval ya quedaron ejecutados arriba.")
        raise SystemExit(1)

    print("=" * 80)
    print("RESPUESTA DEL LLM")
    print("=" * 80)
    print(answer)

    print("\n" + "=" * 80)
    print("LECTURA DEL EXPERIMENTO")
    print("Maximo mock no responde cómo calibrar el activo.")
    print("Maximo mock determina qué documentación corresponde al contexto EAM.")
    print("RAG recupera evidencia dentro de esa documentación.")
    print("El LLM integra la evidencia recuperada en una respuesta fundamentada.")
    print("=" * 80)


if __name__ == "__main__":
    main()
