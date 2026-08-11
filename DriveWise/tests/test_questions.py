import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from retrieval.retriever import search
from retrieval.reranker import Reranker
from generation.generator import generate_answer
from retrieval.vector_store import close_client


# ============================================================
# TEST QUESTIONS
# ============================================================

QUESTIONS = [
    {
        "question": "What safety features does the Hyundai Creta have?",
        "expected_section": "Safety"
    },
    {
        "question": "What are the engine options of the Hyundai Creta?",
        "expected_section": "Performance"
    },
    {
        "question": "What connectivity features does the Hyundai Creta offer?",
        "expected_section": "Connectivity"
    },
    {
        "question": "What interior features are available in the Hyundai Creta?",
        "expected_section": "Interior"
    },
    {
        "question": "What exterior features does the Hyundai Creta have?",
        "expected_section": "Exterior"
    },
    {
        "question": "What colours are available for the Hyundai Creta?",
        "expected_section": "Colours"
    },
    {
        "question": "What ADAS features are available in the Hyundai Creta?",
        "expected_section": "ADAS"
    },
    {
        "question": "What variants of the Hyundai Creta are available?",
        "expected_section": None
    },
    {
        "question": "What is the mileage of the Hyundai Creta?",
        "expected_section": None
    },
    {
        "question": "What is the population of India?",
        "expected_section": None
    }
]


# ============================================================
# CONFIGURATION
# ============================================================

BRAND = "Hyundai"
MODEL = "Creta"

RETRIEVAL_TOP_K = 10
RERANK_TOP_K = 5


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 70)
    print("DRIVE WISE - RAG EVALUATION")
    print("=" * 70)

    reranker = Reranker()

    passed = 0
    failed = 0

    try:

        for index, item in enumerate(
            QUESTIONS,
            start=1
        ):

            question = item["question"]
            expected_section = item["expected_section"]

            print("\n" + "-" * 70)
            print(f"TEST {index}")
            print(f"Question: {question}")
            print("-" * 70)

            # ------------------------------------------------
            # RETRIEVAL
            # ------------------------------------------------

            candidates = search(
                query=question,
                brand=BRAND,
                model=MODEL,
                top_k=RETRIEVAL_TOP_K
            )

            print(
                f"Retrieved: {len(candidates)}"
            )

            if not candidates:

                print("❌ FAIL - No documents retrieved")

                failed += 1
                continue

            # ------------------------------------------------
            # RERANKING
            # ------------------------------------------------

            reranked = reranker.rerank(
                query=question,
                results=candidates,
                top_k=RERANK_TOP_K
            )

            if not reranked:

                print(
                    "❌ FAIL - No relevant results after reranking"
                )

                failed += 1
                continue

            top_score = reranked[0].get(
                "rerank_score",
                0
            )

            print(
                f"Top reranker score: {top_score:.4f}"
            )

            print("\nTop sections:")

            for result in reranked:

                print(
                    f"  - "
                    f"{result.get('section')} "
                    f"(Page {result.get('page_number')})"
                )

            # ------------------------------------------------
            # EVALUATE RETRIEVAL
            # ------------------------------------------------

            if expected_section:

                sections = [
                    str(result.get("section", "")).lower()
                    for result in reranked
                ]

                if expected_section.lower() in sections:

                    print(
                        f"\n✓ Retrieval PASS "
                        f"- {expected_section} section found"
                    )

                    passed += 1

                else:

                    print(
                        f"\n❌ Retrieval FAIL "
                        f"- Expected {expected_section}"
                    )

                    failed += 1

            else:

                print(
                    "\n✓ No expected section "
                    "(manual evaluation required)"
                )

                # We don't automatically mark these as passed
                # because questions such as mileage/variants
                # require checking whether the answer is actually
                # supported by the documents.

            # ------------------------------------------------
            # GENERATION
            # ------------------------------------------------

            print("\nGenerating answer...")

            answer = generate_answer(
                query=question,
                results=reranked
            )

            print("\nANSWER:")
            print(answer)

    finally:

        close_client()

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Total tests: {len(QUESTIONS)}"
    )

    if passed + failed > 0:

        score = (
            passed /
            (passed + failed)
        ) * 100

        print(
            f"Retrieval score: {score:.1f}%"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()