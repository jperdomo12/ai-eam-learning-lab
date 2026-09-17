from __future__ import annotations

import contextlib
import os
import sys
import time

from mcp.server.fastmcp import FastMCP

from step04_semantic_retrieval import DEFAULT_MODEL, semantic_rank
from step04b_semantic_retrieval_content_filter import classify_record
from step08_generate_grounded_answer import GENERATION_TOP_K
from step09_resolve_maximo_doclinks import (
    MAXIMO_MOCK_DIR,
    find_asset,
    load_json,
    resolve_documents,
)
from step10_eam_context_to_rag import build_scoped_chunk_records
from step11_transactional_plus_rag import OPEN_STATUSES, find_asset_workorders


mcp = FastMCP("AI-EAM RAG Learning Lab")

_embedding_model = None


def get_embedding_model():
    """Carga MiniLM una sola vez y lo reutiliza durante toda la sesión MCP."""
    global _embedding_model
    if _embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Falta la dependencia 'sentence-transformers'. "
                "Ejecuta: python -m pip install -r rag/requirements.txt"
            ) from exc

        # MCP por stdio reserva stdout para el protocolo. Cualquier salida incidental
        # de la carga del modelo se redirige a stderr para no interferir con JSON-RPC.
        os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
        with contextlib.redirect_stdout(sys.stderr):
            _embedding_model = SentenceTransformer(DEFAULT_MODEL)

    return _embedding_model


def _load_asset_context(assetnum: str, siteid: str):
    assets = load_json(MAXIMO_MOCK_DIR / "assets.json")
    asset = find_asset(assets, assetnum, siteid)
    if not asset:
        return None
    return asset


@mcp.tool()
def consultar_ots_abiertas_activo(assetnum: str, siteid: str) -> str:
    """
    Consulta las órdenes de trabajo abiertas simuladas de IBM Maximo para un activo y sitio.

    Usa esta Tool para preguntas sobre OTs abiertas, trabajos en curso/aprobados/en espera,
    estados, tipos de trabajo y prioridades. Esta capacidad usa datos estructurados exactos
    del mock WORKORDER; NO utiliza embeddings ni RAG.

    Args:
        assetnum: identificador funcional del activo, por ejemplo PT-201.
        siteid: sitio Maximo, por ejemplo PLANTA1.
    """
    assetnum = assetnum.strip().upper()
    siteid = siteid.strip().upper()

    asset = _load_asset_context(assetnum, siteid)
    if not asset:
        return f"[MAXIMO]\nActivo no encontrado: ASSETNUM={assetnum}, SITEID={siteid}."

    workorders = load_json(MAXIMO_MOCK_DIR / "workorders.json")
    asset_workorders = find_asset_workorders(workorders, assetnum, siteid)
    open_workorders = [
        workorder
        for workorder in asset_workorders
        if workorder.get("status", "").upper() in OPEN_STATUSES
    ]

    lines = [
        "[MAXIMO]",
        "Fuente: WORKORDER simulado",
        f"ASSETNUM: {assetnum}",
        f"SITEID: {siteid}",
        f"OTs totales del activo/sitio: {len(asset_workorders)}",
        f"OTs abiertas: {len(open_workorders)}",
        f"Estados considerados abiertos en esta baseline: {', '.join(sorted(OPEN_STATUSES))}",
    ]

    if not open_workorders:
        lines.append("No se encontraron órdenes de trabajo abiertas en esta baseline.")
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
            ]
        )

    return "\n".join(lines)


@mcp.tool()
def buscar_documentacion_activo(assetnum: str, siteid: str, pregunta: str) -> str:
    """
    Busca conocimiento técnico dentro de la documentación asociada por Doclinks a un activo Maximo simulado.

    Usa esta Tool para preguntas sobre manuales, procedimientos, seguridad, inspección,
    calibración o conocimiento técnico documental. Primero resuelve ASSET -> DOCLINKS -> DOCINFO
    y luego ejecuta retrieval semántico únicamente sobre los documentos asociados al activo.
    Devuelve texto original recuperado con su procedencia; NO genera la respuesta final con otro LLM.

    Args:
        assetnum: identificador funcional del activo, por ejemplo PT-201.
        siteid: sitio Maximo, por ejemplo PLANTA1.
        pregunta: pregunta documental que debe buscarse en la documentación asociada.
    """
    assetnum = assetnum.strip().upper()
    siteid = siteid.strip().upper()
    pregunta = pregunta.strip()

    if not pregunta:
        return "No se recibió una pregunta documental utilizable."

    asset = _load_asset_context(assetnum, siteid)
    if not asset:
        return f"Activo no encontrado: ASSETNUM={assetnum}, SITEID={siteid}."

    doclinks = load_json(MAXIMO_MOCK_DIR / "doclinks.json")
    docinfo = load_json(MAXIMO_MOCK_DIR / "docinfo.json")
    documents = resolve_documents(asset, doclinks, docinfo)
    valid_documents = [
        document
        for document in documents
        if document.get("resolved_path") and document.get("exists")
    ]

    if not valid_documents:
        return "No se encontraron documentos FILE existentes asociados al activo."

    records = build_scoped_chunk_records(valid_documents)
    candidates: list[dict] = []
    for record in records:
        role, reason = classify_record(record)
        if role == "content":
            candidates.append({**record, "role": role, "reason": reason})

    if not candidates:
        return "Los documentos asociados no produjeron chunks de contenido recuperables."

    try:
        model = get_embedding_model()
        ranked, _ = semantic_rank(model, candidates, pregunta)
    except Exception as exc:
        return f"Error al ejecutar retrieval semántico: {type(exc).__name__}: {exc}"

    top_k = min(GENERATION_TOP_K, len(ranked))
    results = ranked[:top_k]

    lines = [
        "[RAG]",
        f"ASSETNUM: {assetnum}",
        f"SITEID: {siteid}",
        f"Documentos asociados por Doclinks: {len(valid_documents)}",
        f"Pregunta documental: {pregunta}",
        f"Top-k recuperado: {top_k}",
    ]

    for position, result in enumerate(results, start=1):
        lines.extend(
            [
                "",
                f"[FUENTE {position}]",
                f"Documento: {result['document']}",
                f"DOCUMENT Maximo: {result['maximo_document']}",
                f"DOCINFOID: {result['docinfoid']}",
                f"Sección: {result['heading']}",
                f"Chunk: {result['chunk']}",
                "Contenido:",
                result["content"],
            ]
        )

    return "\n".join(lines)


if __name__ == "__main__":
    # Diagnóstico local 2026-09-17: el mismo modelo tarda ~46.7 s en cargar desde
    # este intérprete, pero la carga perezosa dentro de una Tool MCP agotó incluso
    # un timeout de 180 s. Para evitar inicializar PyTorch/SentenceTransformer dentro
    # del request síncrono de FastMCP, precalentamos el modelo en el hilo principal
    # antes de iniciar el loop stdio. Luego ambas Tools reutilizan la misma instancia.
    started = time.perf_counter()
    print(
        f"[eam-rag-lab] Pre-cargando modelo de embeddings: {DEFAULT_MODEL}",
        file=sys.stderr,
        flush=True,
    )
    try:
        get_embedding_model()
    except Exception as exc:
        print(
            f"[eam-rag-lab] Error al precargar embeddings: {type(exc).__name__}: {exc}",
            file=sys.stderr,
            flush=True,
        )
        raise

    elapsed = time.perf_counter() - started
    print(
        f"[eam-rag-lab] Modelo listo en {elapsed:.1f} s. Iniciando MCP stdio.",
        file=sys.stderr,
        flush=True,
    )
    mcp.run()
