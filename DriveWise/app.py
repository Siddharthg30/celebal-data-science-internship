import time

from flask import Flask, render_template, request, jsonify

from retrieval.retriever import search
from retrieval.reranker import Reranker
from generation.generator import generate_answer
from retrieval.vector_store import close_client


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)


# ============================================================
# CONFIGURATION
# ============================================================

# CrossEncoder scores are NOT probabilities.
#
# Based on your current testing:
#
# Relevant:
#     +10.08
#
# Clearly irrelevant:
#     -0.69
#
# We will start with a conservative threshold.
# We will validate it with multiple questions later.

RELEVANCE_THRESHOLD = 0.0

RETRIEVAL_TOP_K = 10
RERANK_TOP_K = 5


# ============================================================
# LOAD RERANKER ONCE
# ============================================================

reranker = Reranker()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "DriveWise",
        "gemini_enabled": True
    })


# ============================================================
# CHAT API
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    start_time = time.perf_counter()

    try:

        # ----------------------------------------------------
        # 1. READ REQUEST
        # ----------------------------------------------------

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "error": "Invalid JSON request."
            }), 400


        query = data.get(
            "query",
            ""
        ).strip()

        brand = data.get("brand")
        model = data.get("model")


        # ----------------------------------------------------
        # 2. VALIDATE QUERY
        # ----------------------------------------------------

        if not query:

            return jsonify({
                "success": False,
                "error": "Query cannot be empty."
            }), 400


        if len(query) < 2:

            return jsonify({
                "success": False,
                "error": "Query is too short."
            }), 400


        if len(query) > 500:

            return jsonify({
                "success": False,
                "error": "Query is too long. Maximum 500 characters."
            }), 400


        print("\n" + "=" * 70)
        print("DRIVEWISE REQUEST")
        print("=" * 70)

        print(f"Query: {query}")
        print(f"Brand: {brand}")
        print(f"Model: {model}")


        # ----------------------------------------------------
        # 3. RETRIEVAL
        # ----------------------------------------------------

        candidates = search(

            query=query,

            brand=brand,

            model=model,

            top_k=RETRIEVAL_TOP_K
        )


        print(
            f"Retrieved candidates: {len(candidates)}"
        )


        # ----------------------------------------------------
        # 4. HANDLE NO RETRIEVAL RESULTS
        # ----------------------------------------------------

        if not candidates:

            latency = time.perf_counter() - start_time

            print("Retrieval: NO RESULTS")
            print(f"Latency: {latency:.2f}s")

            return jsonify({

                "success": True,

                "query": query,

                "answer": (
                    "I couldn't find relevant information "
                    "about this in the provided vehicle documents."
                ),

                "sources": [],

                "metadata": {
                    "retrieved": 0,
                    "reranked": 0,
                    "top_reranker_score": None,
                    "gemini_called": False,
                    "relevance": "rejected",
                    "latency_seconds": round(
                        latency,
                        3
                    )
                }

            })


        # ----------------------------------------------------
        # 5. RERANKING
        # ----------------------------------------------------

        reranked = reranker.rerank(

            query=query,

            results=candidates,

            top_k=RERANK_TOP_K
        )


        print(
            f"Reranked results: {len(reranked)}"
        )


        # ----------------------------------------------------
        # 6. HANDLE NO RERANKED RESULTS
        # ----------------------------------------------------

        if not reranked:

            latency = time.perf_counter() - start_time

            print("Reranking: NO RESULTS")
            print(f"Latency: {latency:.2f}s")

            return jsonify({

                "success": True,

                "query": query,

                "answer": (
                    "I couldn't find relevant information "
                    "about this in the provided vehicle documents."
                ),

                "sources": [],

                "metadata": {
                    "retrieved": len(candidates),
                    "reranked": 0,
                    "top_reranker_score": None,
                    "gemini_called": False,
                    "relevance": "rejected",
                    "latency_seconds": round(
                        latency,
                        3
                    )
                }

            })


        # ----------------------------------------------------
        # 7. RELEVANCE CHECK
        # ----------------------------------------------------

        top_score = float(
            reranked[0].get(
                "rerank_score",
                -999
            )
        )


        print(
            f"Top reranker score: {top_score:.4f}"
        )


        if top_score < RELEVANCE_THRESHOLD:

            print(
                "⚠ Query considered insufficiently relevant."
            )


            latency = time.perf_counter() - start_time


            return jsonify({

                "success": True,

                "query": query,

                "answer": (
                    "I couldn't find relevant information "
                    "about this in the provided vehicle documents."
                ),

                "sources": [],

                "metadata": {

                    "retrieved": len(candidates),

                    "reranked": len(reranked),

                    "top_reranker_score": round(
                        top_score,
                        4
                    ),

                    "gemini_called": False,

                    "relevance": "rejected",

                    "latency_seconds": round(
                        latency,
                        3
                    )
                }

            })


        # ----------------------------------------------------
        # 8. SELECT RELEVANT SOURCES
        # ----------------------------------------------------

        relevant_results = [

            result

            for result in reranked

            if float(
                result.get(
                    "rerank_score",
                    -999
                )
            ) >= RELEVANCE_THRESHOLD

        ]


        print(
            f"Relevant sources: {len(relevant_results)}"
        )


        # ----------------------------------------------------
        # 9. GEMINI GENERATION
        # ----------------------------------------------------

        print(
            "Generating answer with Gemini..."
        )


        answer = generate_answer(

            query=query,

            results=relevant_results

        )


        gemini_called = True


        # ----------------------------------------------------
        # 10. SOURCES
        # ----------------------------------------------------

        sources = []


        for result in relevant_results:

            sources.append({

                "chunk_id":
                    result.get("chunk_id"),

                "model":
                    result.get("model"),

                "section":
                    result.get("section"),

                "page_number":
                    result.get("page_number"),

                "source_file":
                    result.get("source_file"),

                "score":
                    result.get("rerank_score")

            })


        # ----------------------------------------------------
        # 11. MONITORING
        # ----------------------------------------------------

        latency = time.perf_counter() - start_time


        print("\n" + "-" * 70)

        print(
            f"Top reranker score: {top_score:.4f}"
        )

        print(
            f"Relevant sources: {len(relevant_results)}"
        )

        print(
            f"Gemini: {'SUCCESS' if gemini_called else 'NOT CALLED'}"
        )

        print(
            f"Latency: {latency:.2f}s"
        )

        print("-" * 70)


        # ----------------------------------------------------
        # 12. API RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "query": query,

            "answer": answer,

            "sources": sources,

            "metadata": {

                "retrieved":
                    len(candidates),

                "reranked":
                    len(reranked),

                "relevant":
                    len(relevant_results),

                "top_reranker_score":
                    round(
                        top_score,
                        4
                    ),

                "gemini_called":
                    gemini_called,

                "relevance":
                    "accepted",

                "latency_seconds":
                    round(
                        latency,
                        3
                    )
            }

        })


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        latency = time.perf_counter() - start_time

        print(
            f"\n❌ API Error: {e}"
        )

        print(
            f"Latency: {latency:.2f}s"
        )


        return jsonify({

            "success": False,

            "error":
                "An error occurred while processing your question."

        }), 500


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        app.run(
            host="0.0.0.0",
            port=5000,
            debug=True,
            use_reloader=False
        )
    finally:
        close_client()