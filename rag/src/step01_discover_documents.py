from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MOCK_FILE = REPO_ROOT / "rag" / "data" / "maximo" / "asset_doclinks_mock.json"


def load_catalog() -> dict:
    with MOCK_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def discover_documents(assetnum: str, siteid: str | None = None) -> list[dict]:
    catalog = load_catalog()

    for asset in catalog["assets"]:
        if asset["assetnum"].upper() != assetnum.upper():
            continue
        if siteid and asset["siteid"].upper() != siteid.upper():
            continue

        documents = []
        for document in asset["documents"]:
            if not document.get("current", True):
                continue

            resolved_path = REPO_ROOT / document["path"]
            documents.append(
                {
                    **document,
                    "assetnum": asset["assetnum"],
                    "siteid": asset["siteid"],
                    "resolved_path": str(resolved_path),
                    "file_exists": resolved_path.exists(),
                }
            )
        return documents

    return []


def main() -> None:
    assetnum = "PT-201"
    siteid = "PLANTA1"

    print("RAG LAB — Paso 01: descubrimiento de documentos desde Maximo (simulado)")
    print(f"Activo: {assetnum} | Sitio: {siteid}\n")

    documents = discover_documents(assetnum, siteid)

    if not documents:
        print("No se encontraron documentos vigentes para el activo.")
        return

    print(f"Documentos vigentes encontrados: {len(documents)}\n")

    for index, document in enumerate(documents, start=1):
        print(f"{index}. {document['description']}")
        print(f"   ID: {document['document_id']}")
        print(f"   Tipo: {document['document_type']}")
        print(f"   Revisión: {document['revision']}")
        print(f"   Ruta: {document['path']}")
        print(f"   Existe en disco: {document['file_exists']}\n")


if __name__ == "__main__":
    main()
