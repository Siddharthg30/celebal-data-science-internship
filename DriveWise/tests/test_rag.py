from retrieval.retriever import search
from retrieval.reranker import Reranker
from retrieval.vector_store import close_client

from generation.generator import generate_answer


QUERY = "What safety features does the Hyundai Creta have?"


def main():

    print("=" * 70)
    print("DRIVE WISE - RAG TEST")
    print("=" * 70)

    # --------------------------------------------------
    # STEP 1: RETRIEVAL
    # --------------------------------------------------

    candidates = search(
        query=QUERY,
        brand="Hyundai",
        model="Creta",
        top_k=10
    )

    print(
        f"\nRetrieved candidates: {len(candidates)}"
    )

    # --------------------------------------------------
    # STEP 2: RERANKING
    # --------------------------------------------------

    reranker = Reranker()

    reranked = reranker.rerank(
        query=QUERY,
        results=candidates,
        top_k=5
    )

    print(
        f"Reranked results: {len(reranked)}"
    )

    # --------------------------------------------------
    # STEP 3: GEMINI GENERATION
    # --------------------------------------------------

    print("\nGenerating answer with Gemini...")

    answer = generate_answer(
        query=QUERY,
        results=reranked
    )

    # --------------------------------------------------
    # STEP 4: DISPLAY
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("DRIVEWISE ANSWER")
    print("=" * 70)

    print("\n" + answer)


if __name__ == "__main__":

    try:
        main()

    finally:
        close_client()