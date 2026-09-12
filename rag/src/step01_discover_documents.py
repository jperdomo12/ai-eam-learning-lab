from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_DOCUMENTS_DIR = REPO_ROOT / "rag" / "data" / "source_documents"

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf", ".docx", ".html", ".htm"}


def discover_documents(folder: Path) -> list[Path]:
    """Devuelve archivos soportados presentes directamente en una carpeta local."""
    if not folder.exists():
        raise FileNotFoundError(f"La carpeta no existe: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"La ruta no es una carpeta: {folder}")

    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def main() -> None:
    folder = (
        Path(sys.argv[1]).expanduser().resolve()
        if len(sys.argv) > 1
        else DEFAULT_SOURCE_DOCUMENTS_DIR
    )

    print("RAG LAB — Paso 01: descubrimiento de documentos desde una carpeta local")
    print(f"Carpeta fuente: {folder}\n")

    documents = discover_documents(folder)

    if not documents:
        print("No se encontraron documentos soportados en la carpeta.")
        return

    print(f"Documentos encontrados: {len(documents)}\n")

    for index, document in enumerate(documents, start=1):
        print(f"{index}. {document.name}")
        print(f"   Formato: {document.suffix.lower() or '(sin extensión)'}")
        print(f"   Ruta: {document}\n")


if __name__ == "__main__":
    main()
