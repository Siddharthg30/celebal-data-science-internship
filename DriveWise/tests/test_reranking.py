from retrieval.retriever import search
from retrieval.reranker import Reranker


QUERY = "What safety features does this car have?"


def display_results(title, results):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    for i, result in enumerate(results, 1):

        print(
            f"\n[{i}] "
            f"Rerank Score: "
            f"{result.get('rerank_score', 'N/A')}"
        )

        print(
            f"Vector Score: "
            f"{result.get('score', 'N/A')}"
        )

        print(
            f"Model: {result['model']}"
        )

        print(
            f"Section: {result['section']}"
        )

        print(
            f"Page: {result['page_number']}"
        )

        print(
            f"Chunk: {result['chunk_id']}"
        )

        print(
            result["text"][:300]
        )


def main():

    print("=" * 70)
    print("DRIVE WISE - RETRIEVAL + RERANKING TEST")
    print("=" * 70)

    # ------------------------------------------
    # STEP 1: Retrieve candidates
    # ------------------------------------------

    candidates = search(
        query=QUERY,
        brand="Hyundai",
        model="Creta",
        top_k=10
    )

    print(
        f"\nRetrieved candidates: {len(candidates)}"
    )

    display_results(
        "BEFORE RERANKING",
        candidates
    )

    # ------------------------------------------
    # STEP 2: Rerank
    # ------------------------------------------

    reranker = Reranker()

    reranked = reranker.rerank(
        query=QUERY,
        results=candidates,
        top_k=5
    )

    # ------------------------------------------
    # STEP 3: Display
    # ------------------------------------------

    display_results(
        "AFTER RERANKING",
        reranked
    )


if __name__ == "__main__":
    main()