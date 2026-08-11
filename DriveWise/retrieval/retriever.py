from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue
)

from retrieval.vector_store import get_client
from retrieval.embedding import embedding_model


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

COLLECTION_NAME = "drive_wise_cars"


# --------------------------------------------------
# METADATA FILTER
# --------------------------------------------------

def build_filter(brand=None, model=None):

    conditions = []

    if brand:
        conditions.append(
            FieldCondition(
                key="brand",
                match=MatchValue(value=brand)
            )
        )

    if model:
        conditions.append(
            FieldCondition(
                key="model",
                match=MatchValue(value=model)
            )
        )

    if not conditions:
        return None

    return Filter(must=conditions)


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

def search(
    query,
    brand=None,
    model=None,
    top_k=10
):

    # Get shared Qdrant client
    client = get_client()

    # Create query embedding
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Build metadata filter
    query_filter = build_filter(
        brand=brand,
        model=model
    )

    # Vector search
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=query_filter,
        limit=top_k,
        with_payload=True
    ).points

    # Format results
    formatted_results = []

    for result in results:

        payload = result.payload

        formatted_results.append({

            "score": result.score,

            "chunk_id":
                payload.get("chunk_id"),

            "text":
                payload.get("text"),

            "brand":
                payload.get("brand"),

            "model":
                payload.get("model"),

            "section":
                payload.get("section"),

            "page_number":
                payload.get("page_number"),

            "source_file":
                payload.get("source_file"),

            "document_id":
                payload.get("document_id")
        })

    return formatted_results


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

def display_results(results):

    print("\n" + "=" * 70)
    print("RETRIEVAL RESULTS")
    print("=" * 70)

    if not results:
        print("No results found.")
        return

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n[{index}] "
            f"Score: {result['score']:.4f}"
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
            f"Source: {result['source_file']}"
        )

        print(
            f"\n{result['text'][:500]}"
        )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    query = "What safety features does this car have?"

    print("\n" + "=" * 70)
    print("TEST: METADATA-FILTERED CRETA SEARCH")
    print("=" * 70)

    results = search(
        query=query,
        brand="Hyundai",
        model="Creta",
        top_k=5
    )

    display_results(results)