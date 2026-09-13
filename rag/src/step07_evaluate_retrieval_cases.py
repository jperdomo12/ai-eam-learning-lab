from __future__ import annotations

import json
from pathlib import Path

from step02_read_and_chunk import REPO_ROOT
from step06_build_grounded_context import retrieve_top_k


CASES_PATH = REPO_ROOT / "rag" / "data" / "evaluation_cases.json"


def load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def evaluate_expected_headings(results: list[dict], expected_headings: list[str]) -> tuple[int, list[str]]:
    retrieved_headings = {result["heading"] for result in results}
    missing = [heading for heading in expected_headings if heading not in retrieved_headings]
    return len(expected_headings) - len(missing), missing


def main() -> None:
    print("RAG LAB — Paso 07A: baseline de evaluación del retrieval")
    print(f"Casos: {CASES_PATH}\n")
    print("Objetivo de aprendizaje:")
    print("- ejecutar un conjunto pequeño y reproducible de casos A–D")
    print("- observar retrieval correcto, formulaciones distintas e información repartida")
    print("- incluir un caso sin respuesta para estudiar abstención")
    print("- NO decidir automáticamente si existe evidencia suficiente solo por similarity\n")

    cases = load_cases()

    for case in cases:
        print("=" * 80)
        print(f"CASO {case['id']} — {case['name']}")
        print(f"Pregunta: {case['question']}")
        print(f"Respuesta esperada disponible: {'SÍ' if case['expected_answerable'] else 'NO'}")
        print(f"Nota: {case['notes']}\n")

        results = retrieve_top_k(case["question"])

        print("Top-k recuperado:")
        for position, result in enumerate(results, start=1):
            print(
                f"#{position} | {result['similarity']:.4f} | "
                f"{result['document']} | chunk {result['chunk']} | {result['heading']}"
            )

        expected_headings = case.get("expected_headings", [])
        if expected_headings:
            hits, missing = evaluate_expected_headings(results, expected_headings)
            print("\nChequeo pedagógico de headings esperados:")
            print(f"- recuperados: {hits}/{len(expected_headings)}")
            if missing:
                for heading in missing:
                    print(f"- faltante: {heading}")
            else:
                print("- todos los headings esperados aparecen en el Top-k")
        else:
            print("\nChequeo pedagógico:")
            print("- este caso NO tiene una respuesta esperada en los documentos")
            print("- aunque exista Top-k, debe revisarse si el contexto realmente contiene la respuesta")

        print()

    print("=" * 80)
    print("IDEA CLAVE")
    print("Top-k encontrado no equivale a respuesta encontrada.")
    print("La similarity sirve para ranking, no es una prueba automática de suficiencia de evidencia.")
    print("Este baseline se reutilizará cuando conectemos un LLM para evaluar generación y abstención.")
    print("=" * 80)


if __name__ == "__main__":
    main()
