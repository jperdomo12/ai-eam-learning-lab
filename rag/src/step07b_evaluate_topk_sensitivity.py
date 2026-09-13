from __future__ import annotations

import json

import numpy as np

from step02_read_and_chunk import REPO_ROOT
from step04_semantic_retrieval import load_embedding_model
from step05_query_vector_index import load_index


CASES_PATH = REPO_ROOT / "rag" / "data" / "evaluation_cases.json"
TOP_K_VALUES = [1, 2, 3, 4, 5]


def load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def rank_all(query: str, embeddings: np.ndarray, metadata: list[dict], model) -> list[dict]:
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    scores = embeddings @ query_embedding
    ranked = [
        {**record, "similarity": float(score)}
        for record, score in zip(metadata, scores)
    ]
    ranked.sort(key=lambda item: item["similarity"], reverse=True)
    return ranked


def evidence_coverage(results: list[dict], groups: list[dict]) -> tuple[int, list[str]]:
    headings = {result["heading"] for result in results}
    covered = 0
    missing: list[str] = []

    for group in groups:
        acceptable = set(group["acceptable_headings"])
        if headings & acceptable:
            covered += 1
        else:
            missing.append(group["name"])

    return covered, missing


def main() -> None:
    print("RAG LAB — Paso 07B: sensibilidad a Top-k")
    print(f"Casos: {CASES_PATH}\n")
    print("Objetivo de aprendizaje:")
    print("- mantener fijo modelo, embeddings, documentos y consultas")
    print("- variar únicamente cuántos chunks recuperamos: k = 1..5")
    print("- observar el compromiso entre cobertura de evidencia y contexto adicional")
    print("- evitar asumir que un Top-k mayor siempre es mejor\n")

    embeddings, metadata, manifest = load_index()
    model = load_embedding_model(manifest["model"])
    cases = load_cases()

    for case in cases:
        print("=" * 80)
        print(f"CASO {case['id']} — {case['name']}")
        print(f"Pregunta: {case['question']}")
        print(f"Respuesta esperada disponible: {'SÍ' if case['expected_answerable'] else 'NO'}")

        ranked = rank_all(case["question"], embeddings, metadata, model)
        groups = case.get("expected_evidence_groups", [])

        if not case["expected_answerable"]:
            print("Este caso no tiene respuesta documental conocida.")
            print("Se muestran los primeros 5 resultados, pero NO se interpreta cobertura como answerability:\n")
            for position, result in enumerate(ranked[:5], start=1):
                print(
                    f"#{position} | {result['similarity']:.4f} | "
                    f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
                )
            print()
            continue

        print(f"Grupos de evidencia esperados: {len(groups)}")
        for group in groups:
            alternatives = " | ".join(group["acceptable_headings"])
            print(f"- {group['name']}: {alternatives}")
        print()

        for k in TOP_K_VALUES:
            results = ranked[:k]
            covered, missing = evidence_coverage(results, groups)
            status = "COMPLETA" if covered == len(groups) else "INCOMPLETA"
            print(
                f"k={k} | cobertura={covered}/{len(groups)} | {status} | "
                f"chunks enviados={len(results)}"
            )
            if missing:
                print(f"     faltante: {', '.join(missing)}")

        print("\nRanking de referencia — primeros 5:")
        for position, result in enumerate(ranked[:5], start=1):
            print(
                f"#{position} | {result['similarity']:.4f} | "
                f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
            )
        print()

    print("=" * 80)
    print("IDEA CLAVE")
    print("Top-k controla cuánta evidencia candidata pasa a la siguiente etapa.")
    print("Aumentar k puede mejorar recall/cobertura, pero también añade ruido, tokens y coste.")
    print("No existe un k universalmente correcto: debe evaluarse con casos representativos.")
    print("=" * 80)


if __name__ == "__main__":
    main()
