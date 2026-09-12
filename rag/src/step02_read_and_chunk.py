from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_DIR = REPO_ROOT / "rag" / "data" / "source_documents"
SUPPORTED_TEXT_EXTENSIONS = {".md", ".txt"}
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def discover_text_documents(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"La carpeta no existe: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"La ruta no es una carpeta: {folder}")

    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS
    )


def read_text(document: Path) -> str:
    return document.read_text(encoding="utf-8")


def chunk_markdown_by_headings(text: str) -> list[dict[str, str]]:
    """Divide Markdown por encabezados para hacer el chunking visible y explicable."""
    chunks: list[dict[str, str]] = []
    current_heading = "SIN ENCABEZADO"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        content = "\n".join(current_lines).strip()
        if content:
            chunks.append({"heading": current_heading, "content": content})
        current_lines = []

    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            flush()
            current_heading = match.group(2).strip()
            continue
        current_lines.append(line)

    flush()
    return chunks


def chunk_plain_text(text: str) -> list[dict[str, str]]:
    """Baseline simple para TXT: cada bloque separado por línea en blanco es un chunk."""
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    return [
        {"heading": f"BLOQUE {index}", "content": block}
        for index, block in enumerate(blocks, start=1)
    ]


def create_chunks(document: Path) -> list[dict[str, str]]:
    text = read_text(document)
    if document.suffix.lower() == ".md":
        return chunk_markdown_by_headings(text)
    return chunk_plain_text(text)


def main() -> None:
    folder = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else DEFAULT_SOURCE_DIR

    print("RAG LAB — Paso 02: lectura y chunking visible")
    print(f"Carpeta fuente: {folder}\n")
    print("Baseline de aprendizaje:")
    print("- Markdown (.md): un chunk por sección/encabezado")
    print("- Texto (.txt): un chunk por bloque separado por línea en blanco")
    print("- Todavía NO usamos embeddings ni búsqueda semántica.\n")

    documents = discover_text_documents(folder)

    if not documents:
        print("No se encontraron documentos .md o .txt para este paso.")
        return

    total_chunks = 0

    for document in documents:
        chunks = create_chunks(document)
        total_chunks += len(chunks)

        print("=" * 80)
        print(f"DOCUMENTO: {document.name}")
        print(f"CHUNKS: {len(chunks)}")
        print("=" * 80)

        for index, chunk in enumerate(chunks, start=1):
            content = chunk["content"]
            print(f"\n[{document.name} | chunk {index}]")
            print(f"Sección: {chunk['heading']}")
            print(f"Caracteres: {len(content)}")
            print("-" * 80)
            print(content)

        print()

    print("=" * 80)
    print(f"RESUMEN: {len(documents)} documento(s) → {total_chunks} chunk(s)")
    print("=" * 80)


if __name__ == "__main__":
    main()
