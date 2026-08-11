import sys
import json
from pathlib import Path

# Allow execution from the DriveWise project root:
# python evaluation/ragas_evaluation.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from retrieval.retriever import search
from retrieval.reranker import Reranker
from generation.generator import generate_answer
from retrieval.vector_store import close_client

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)


QUESTIONS_FILE = Path(__file__).resolve().parent / "evaluation_questions.json"

BRAND = "Hyundai"
MODEL = "Creta"

RETRIEVAL_TOP_K = 10
RERANK_TOP_K = 5


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("=" * 70)
    print("DRIVEWISE - RAGAS EVALUATION")
    print("=" * 70)

    questions = load_questions()
    reranker = Reranker()

    dataset_rows = []

    try:
        for index, item in enumerate(questions, start=1):
            question = item["question"]

            print("\n" + "-" * 70)
            print(f"TEST {index}/{len(questions)}")
            print(f"Question: {question}")
            print("-" * 70)

            candidates = search(
                query=question,
                brand=BRAND,
                model=MODEL,
                top_k=RETRIEVAL_TOP_K,
            )

            print(f"Retrieved candidates: {len(candidates)}")

            reranked = reranker.rerank(
                query=question,
                results=candidates,
                top_k=RERANK_TOP_K,
            )

            print(f"Reranked results: {len(reranked)}")

            if reranked:
                print(
                    f"Top reranker score: "
                    f"{reranked[0].get('rerank_score', 0):.4f}"
                )

            # Keep only the actual retrieved document text.
            contexts = []

            for result in reranked:
                text = (result.get("text") or "").strip()

                if text:
                    contexts.append(text)

            # Generate using the exact existing DriveWise generation pipeline.
            answer = generate_answer(
                query=question,
                results=reranked,
            )

            print("\nANSWER:")
            print(answer)

            # RAGAS expects one row containing:
            # user_input, response, retrieved_contexts, reference
            dataset_rows.append(
                {
                    "user_input": question,
                    "response": answer,
                    "retrieved_contexts": contexts,
                    "reference": item["ground_truth"],
                }
            )

    finally:
        close_client()

    if not dataset_rows:
        print("\nNo evaluation records were generated.")
        return

    print("\n" + "=" * 70)
    print("RUNNING RAGAS")
    print("=" * 70)

    dataset = Dataset.from_list(dataset_rows)

    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    print("\n" + "=" * 70)
    print("DRIVEWISE RAGAS RESULTS")
    print("=" * 70)

    print(result)

    # Save results in a simple JSON-compatible format.
    try:
        result_df = result.to_pandas()
        output_file = Path(__file__).resolve().parent / "ragas_results.csv"
        result_df.to_csv(output_file, index=False)

        print(f"\nDetailed results saved to: {output_file}")

    except Exception as error:
        print(f"\nCould not save detailed CSV results: {error}")

    print("=" * 70)


if __name__ == "__main__":
    main()
