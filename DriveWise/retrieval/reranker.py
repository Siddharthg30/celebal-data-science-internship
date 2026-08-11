from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
MIN_RERANK_SCORE = 0.0


class Reranker:

    def __init__(self, model_name=MODEL_NAME):

        print("Loading reranker model...")

        self.model = CrossEncoder(model_name)

        print("✓ Reranker loaded")


    def rerank(
        self,
        query,
        results,
        top_k=5
    ):

        if not results:
            return []

        pairs = [
            (query, result["text"])
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(results, scores):

            result_copy = result.copy()

            result_copy["rerank_score"] = float(score)

            reranked_results.append(result_copy)

        reranked_results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        # --------------------------------------------------
        # RELEVANCE GATE
        # --------------------------------------------------

        top_score = reranked_results[0]["rerank_score"]

        print(
            f"\nTop reranker score: {top_score:.4f}"
        )

        if top_score < MIN_RERANK_SCORE:

            print(
                "⚠ Query considered insufficiently relevant."
            )

            return []

        return reranked_results[:top_k]