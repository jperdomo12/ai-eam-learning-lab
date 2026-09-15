from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MAXIMO_MOCK_DIR = REPO_ROOT / "rag" / "data" / "maximo_mock"

# Baseline pedagógica elegida para este LAB:
# Doclinks de ASSET resueltos por ASSETUID (site-specific).
# ASSETID también se conserva en el mock porque Maximo puede usarlo
# en comportamiento/configuración system-level de attached documents.
ASSET_DOCLINK_OWNER_KEY = "assetuid"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_asset(assets, assetnum: str, siteid: str):
    for asset in assets:
        if (
            asset.get("assetnum", "").upper() == assetnum.upper()
            and asset.get("siteid", "").upper() == siteid.upper()
        ):
            return asset
    return None


def resolve_documents(asset, doclinks, docinfo):
    owner_id = asset[ASSET_DOCLINK_OWNER_KEY]
    links = [
        link
        for link in doclinks
        if link.get("ownertable", "").upper() == "ASSET"
        and link.get("ownerid") == owner_id
    ]

    docinfo_by_id = {doc["docinfoid"]: doc for doc in docinfo}
    resolved = []

    for link in links:
        doc = docinfo_by_id.get(link.get("docinfoid"))
        if not doc:
            continue

        path_value = None
        exists = None
        if doc.get("urltype", "").upper() == "FILE":
            candidate = Path(doc["urlname"])
            if not candidate.is_absolute():
                candidate = REPO_ROOT / candidate
            path_value = candidate
            exists = candidate.exists()

        resolved.append(
            {
                "doclinksid": link["doclinksid"],
                "docinfoid": doc["docinfoid"],
                "document": doc["document"],
                "description": doc["description"],
                "doctype": doc["doctype"],
                "urltype": doc["urltype"],
                "urlname": doc["urlname"],
                "resolved_path": str(path_value) if path_value else None,
                "exists": exists,
            }
        )

    return resolved


def main():
    parser = argparse.ArgumentParser(
        description="Resuelve documentos asociados a un activo usando una simulación mínima de ASSET + DOCLINKS + DOCINFO."
    )
    parser.add_argument("assetnum", nargs="?", default="PT-201")
    parser.add_argument("siteid", nargs="?", default="PLANTA1")
    args = parser.parse_args()

    assets = load_json(MAXIMO_MOCK_DIR / "assets.json")
    doclinks = load_json(MAXIMO_MOCK_DIR / "doclinks.json")
    docinfo = load_json(MAXIMO_MOCK_DIR / "docinfo.json")

    asset = find_asset(assets, args.assetnum, args.siteid)
    if not asset:
        raise SystemExit(
            f"Activo no encontrado: assetnum={args.assetnum}, siteid={args.siteid}"
        )

    documents = resolve_documents(asset, doclinks, docinfo)
    owner_id = asset[ASSET_DOCLINK_OWNER_KEY]

    print("=== MAXIMO MOCK: RESOLUCIÓN DE DOCLINKS ===")
    print(f"ASSETNUM : {asset['assetnum']}")
    print(f"SITEID   : {asset['siteid']}")
    print(f"ASSETUID : {asset['assetuid']}")
    print(f"ASSETID  : {asset['assetid']}")
    print(f"OWNER KEY: {ASSET_DOCLINK_OWNER_KEY.upper()} (baseline site-specific)")
    print(f"OWNERID  : {owner_id}")
    print(f"DESCRIP. : {asset['description']}")
    print()

    if not documents:
        print("No se encontraron documentos asociados al activo.")
        return

    print(f"Documentos asociados: {len(documents)}")
    for index, doc in enumerate(documents, start=1):
        print()
        print(f"[{index}] {doc['document']} — {doc['description']}")
        print(f"    DOCLINKSID : {doc['doclinksid']}")
        print(f"    DOCINFOID  : {doc['docinfoid']}")
        print(f"    DOCTYPE    : {doc['doctype']}")
        print(f"    URLTYPE    : {doc['urltype']}")
        print(f"    URLNAME    : {doc['urlname']}")
        if doc["resolved_path"]:
            print(f"    PATH       : {doc['resolved_path']}")
            print(f"    EXISTE     : {'sí' if doc['exists'] else 'no'}")


if __name__ == "__main__":
    main()
