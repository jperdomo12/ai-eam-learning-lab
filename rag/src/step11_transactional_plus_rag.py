from __future__ import annotations

import argparse
import os

from step04_semantic_retrieval import DEFAULT_MODEL, load_embedding_model, semantic_rank
from step04b_semantic_retrieval_content_filter import classify_record
from step06_build_grounded_context import build_context
from step08_generate_grounded_answer import (
    DEFAULT_GENERATION_MODEL,
    GENERATION_TOP_K,
    generate_with_ollama,
)
from step09_resolve_maximo_doclinks import (
    ASSET_DOCLINK_OWNER_KEY,
    MAXIMO_MOCK_DIR,
    find_asset,
    load_json,
    resolve_documents,
)
from step10_eam_context_to_rag import build_scoped_chunk_records


DEFAULT_ASSETNUM = "PT-201"
DEFAULT_SITEID = "PLANTA1"
DEFAULT_QUERY = (
    "¿Tiene el PT-201 alguna OT abierta y qué indica su documentación "
    "que debo revisar antes de intervenirlo?"
)
DEFAULT_DOCUMENT_QUERY = "¿Qué debo revisar antes de intervenir o calibrar el PT-201?"

# Baseline pedagógica del LAB. En Maximo real pueden existir sinónimos y estados
# configurados; aquí usamos los estados ya empleados en el MCP Lab.
OPEN_STATUSES = {"WAPPR", "APPR", "INPRG", "WMATL"}


def find_asset_workorders(workorders: list[dict], assetnum: str, siteid: str) -> list[dict]:
    return [
        workorder
        for workorder in workorders
        if workorder.get("assetnum", "").upper() == assetnum.upper()
        and workorder.get("siteid", "").upper() == siteid.upper()
    ]


def find_open_workorders(workorders: list[dict], assetnum: str, siteid: str) -> list[dict]:
    return [
        workorder
        for workorder in find_asset_workorders(workorders, assetnum, siteid)
        if workorder.get("status", "").upper() in OPEN_STATUSES
    ]


def build_transactional_context(open_workorders: list[dict]) -> str:
    lines = [
        "[MAXIMO]",
        "Fuente: WORKORDER simulado",
        f"Órdenes de trabajo abiertas encontradas: {len(open_workorders)}",
    ]

    if not open_workorders:
        lines.append("No se encontraron OTs abiertas para el activo y sitio consultados.")
        return "\n".join(lines)

    for workorder in open_workorders:
        lines.extend(
            [
                "",
                f"WONUM: {workorder['wonum']}",
                f"WORKORDERID: {workorder['workorderid']}",
                f"DESCRIPTION: {workorder['description']}",
                f"STATUS: {workorder['status']}",
                f"WORKTYPE: {workorder['worktype']}",
                f"WOPRIORITY: {workorder['wopriority']}",
                f"ASSETNUM: {workorder['assetnum']}",
                f"SITEID: {workorder['siteid']}",
            ]
        )

    return "\n".join(lines)


def build_integrated_prompt(query: str, transactional_context: str, document_context: str) -> str:
    return f"""INSTRUCCIONES
Responde únicamente con base en los DATOS TRANSACCIONALES MAXIMO y el CONTEXTO DOCUMENTAL RECUPERADO.
No inventes estados, órdenes de trabajo, pasos, valores ni condiciones.

Mantén separadas las dos clases de evidencia:
- para hechos operativos de órdenes de trabajo, cita [MAXIMO];
- para indicaciones de manuales/procedimientos, cita [FUENTE 1], [FUENTE 2], etc.;
- si alguna parte de la pregunta no tiene evidencia suficiente, indícalo explícitamente.

PREGUNTA
{query}

DATOS TRANSACCIONALES MAXIMO
{transactional_context}

CONTEXTO DOCUMENTAL RECUPERADO
{document_context}
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Combina datos transaccionales simulados de WORKORDER con RAG documental "
            "acotado por Doclinks para un mismo contexto EAM."
        )
    )
    parser.add_argument("assetnum", nargs="?", default=DEFAULT_ASSETNUM)
    parser.add_argument("siteid", nargs="?", default=DEFAULT_SITEID)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--document-query", default=DEFAULT_DOCUMENT_QUERY)
    args = parser.parse_args()

    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_GENERATION_MODEL)

    assets = load_json(MAXIMO_MOCK_DIR / "assets.json")
    doclinks = load_json(MAXIMO_MOCK_DIR / "doclinks.json")
    docinfo = load_json(MAXIMO_MOCK_DIR / "docinfo.json")
    workorders = load_json(MAXIMO_MOCK_DIR / "workorders.json")

    asset = find_asset(assets, args.assetnum, args.siteid)
    if not asset:
        raise SystemExit(
            f"Activo no encontrado: assetnum={args.assetnum}, siteid={args.siteid}"
        )

    all_asset_workorders = find_asset_workorders(workorders, args.assetnum, args.siteid)
    open_workorders = find_open_workorders(workorders, args.assetnum, args.siteid)
    transactional_context = build_transactional_context(open_workorders)

    documents = resolve_documents(asset, doclinks, docinfo)
    valid_documents = [
        document
        for document in documents
        if document.get("resolved_path") and document.get("exists")
    ]
    if not valid_documents:
        raise SystemExit("No hay documentos FILE existentes asociados al activo.")

    records = build_scoped_chunk_records(valid_documents)
    candidates: list[dict] = []
    for record in records:
        role, reason = classify_record(record)
        if role == "content":
            candidates.append({**record, "role": role, "reason": reason})

    if not candidates:
        raise SystemExit("Los documentos asociados no produjeron chunks recuperables.")

    print("=== PASO 11: DATOS TRANSACCIONALES + RAG DOCUMENTAL ===")
    print(f"ASSETNUM : {asset['assetnum']}")
    print(f"SITEID   : {asset['siteid']}")
    print(f"ASSETUID : {asset['assetuid']}")
    print(f"ASSETID  : {asset['assetid']}")
    print(f"OWNER KEY: {ASSET_DOCLINK_OWNER_KEY.upper()} (baseline site-specific)")
    print(f"Pregunta : {args.query}\n")

    print("1) RUTA TRANSACCIONAL — WORKORDER")
    print(f"OTs del activo/sitio en el mock: {len(all_asset_workorders)}")
    print(f"Estados considerados abiertos en esta baseline: {', '.join(sorted(OPEN_STATUSES))}")
    print(f"OTs abiertas encontradas: {len(open_workorders)}")
    for workorder in all_asset_workorders:
        marker = "ABIERTA" if workorder["status"] in OPEN_STATUSES else "EXCLUIDA"
        print(
            f"- {workorder['wonum']} | status={workorder['status']} | "
            f"priority={workorder['wopriority']} | {marker} | {workorder['description']}"
        )
    print("Nota: esta ruta usa filtrado estructurado exacto; NO usa embeddings ni RAG.\n")

    print("2) RUTA DOCUMENTAL — DOCLINKS + RAG")
    print(f"Documentos asociados por Doclinks: {len(valid_documents)}")
    for document in valid_documents:
        print(f"- {document['document']} | DOCINFOID={document['docinfoid']} | {document['urlname']}")
    print(f"Pregunta documental para retrieval: {args.document_query}")
    print(f"Chunks de contenido candidatos: {len(candidates)}\n")

    model = load_embedding_model(DEFAULT_MODEL)
    ranked, dimensions = semantic_rank(model, candidates, args.document_query)
    top_k = min(GENERATION_TOP_K, len(ranked))
    results = ranked[:top_k]

    print("3) RETRIEVAL DOCUMENTAL")
    print(f"Modelo embeddings: {DEFAULT_MODEL}")
    print(f"Dimensiones: {dimensions}")
    print(f"Top-k efectivo: {top_k}")
    for position, result in enumerate(results, start=1):
        print(
            f"#{position} | similarity={result['similarity']:.4f} | "
            f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
        )

    document_context = build_context(results)
    prompt = build_integrated_prompt(args.query, transactional_context, document_context)

    print("\n4) INTEGRACIÓN EN EL LLM")
    print("El LLM recibe dos entradas diferentes:")
    print("- datos transaccionales exactos del mock WORKORDER")
    print("- texto original recuperado por RAG desde documentos asociados por Doclinks")
    print("Runtime: Ollama")
    print(f"LLM: {model_name}\n")

    try:
        answer = generate_with_ollama(prompt, model_name)
    except Exception as exc:
        print(f"La generación local falló: {type(exc).__name__}: {exc}")
        print("Las rutas transaccional y documental ya quedaron ejecutadas arriba.")
        raise SystemExit(1)

    print("=" * 80)
    print("RESPUESTA DEL LLM")
    print("=" * 80)
    print(answer)

    print("\n" + "=" * 80)
    print("LECTURA DEL EXPERIMENTO")
    print("WORKORDER aporta estado operativo estructurado y actual del mock.")
    print("DOCLINKS determina qué documentos aplican al activo.")
    print("RAG recupera conocimiento dentro de esos documentos.")
    print("El LLM combina ambas clases de evidencia en una sola respuesta.")
    print("No hay agente ni MCP activo en este paso: la orquestación está codificada de forma explícita.")
    print("=" * 80)


if __name__ == "__main__":
    main()
