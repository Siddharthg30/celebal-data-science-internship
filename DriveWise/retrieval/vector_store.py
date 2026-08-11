from pathlib import Path
import json
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from retrieval.embedding import embedding_model


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNK_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "chunks"
)

QDRANT_DIR = (
    BASE_DIR
    / "data"
    / "qdrant"
)

QDRANT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

COLLECTION_NAME = "drive_wise_cars"

VECTOR_SIZE = 384


# --------------------------------------------------
# SHARED QDRANT CLIENT
# --------------------------------------------------

_client = None


def get_client():

    global _client

    if _client is None:

        _client = QdrantClient(
            path=str(QDRANT_DIR)
        )

    return _client


def close_client():

    global _client

    if _client is not None:

        try:
            _client.close()
            print("\n✓ Qdrant client closed")

        except Exception as e:

            print(
                f"\n⚠ Error closing Qdrant client: {e}"
            )

        finally:

            _client = None


# --------------------------------------------------
# CREATE / RESET COLLECTION
# --------------------------------------------------

def create_collection():

    client = get_client()

    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if COLLECTION_NAME in existing_collections:

        print(
            f"Collection '{COLLECTION_NAME}' already exists."
        )

        print("Deleting old collection...")

        client.delete_collection(
            COLLECTION_NAME
        )

    client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    print(
        f"✓ Created collection: {COLLECTION_NAME}"
    )


# --------------------------------------------------
# LOAD CHUNKS
# --------------------------------------------------

def load_all_chunks():

    chunk_files = sorted(
        CHUNK_DIR.glob("*_chunks.json")
    )

    if not chunk_files:

        raise FileNotFoundError(
            f"No chunk files found in {CHUNK_DIR}"
        )

    all_chunks = []

    for file in chunk_files:

        print(
            f"Loading: {file.name}"
        )

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        chunks = data["chunks"]

        all_chunks.extend(chunks)

        print(
            f"  ✓ {len(chunks)} chunks"
        )

    print(
        f"\nTotal chunks: {len(all_chunks)}"
    )

    return all_chunks


# --------------------------------------------------
# CREATE EMBEDDINGS
# --------------------------------------------------

def create_embeddings(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        "\nCreating embeddings..."
    )

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    print(
        f"✓ Created {len(embeddings)} embeddings"
    )

    print(
        f"✓ Vector dimension: {embeddings.shape[1]}"
    )

    return embeddings


# --------------------------------------------------
# INSERT INTO QDRANT
# --------------------------------------------------

def insert_vectors(
    chunks,
    embeddings
):

    client = get_client()

    points = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        point_id = str(uuid.uuid4())

        payload = {

            "chunk_id":
                chunk["chunk_id"],

            "text":
                chunk["text"],

            "document_id":
                chunk["metadata"]["document_id"],

            "brand":
                chunk["metadata"]["brand"],

            "model":
                chunk["metadata"]["model"],

            "document_type":
                chunk["metadata"]["document_type"],

            "source_file":
                chunk["metadata"]["source_file"],

            "page_number":
                chunk["metadata"]["page_number"],

            "section":
                chunk["metadata"]["section"],

            "chunk_index":
                chunk["metadata"]["chunk_index"],

            "word_count":
                chunk["metadata"]["word_count"]
        }

        points.append(

            PointStruct(

                id=point_id,

                vector=embedding.tolist(),

                payload=payload
            )
        )

    print(
        f"\nUploading {len(points)} points..."
    )

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points
    )

    print(
        "✓ Vectors uploaded successfully"
    )


# --------------------------------------------------
# VERIFY COLLECTION
# --------------------------------------------------

def verify_collection():

    client = get_client()

    info = client.get_collection(
        COLLECTION_NAME
    )

    print("\nQDRANT COLLECTION")
    print("-" * 40)

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    print(
        f"Vectors: {info.points_count}"
    )

    print(
        f"Vector size: {VECTOR_SIZE}"
    )

    print(
        "Distance: COSINE"
    )


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def build_vector_store():

    print("=" * 60)
    print("DRIVE WISE - VECTOR DATABASE BUILD")
    print("=" * 60)

    # 1. Create collection
    create_collection()

    # 2. Load chunks
    chunks = load_all_chunks()

    # 3. Generate embeddings
    embeddings = create_embeddings(
        chunks
    )

    # 4. Insert vectors
    insert_vectors(
        chunks,
        embeddings
    )

    # 5. Verify
    verify_collection()

    print("\n" + "=" * 60)
    print("VECTOR DATABASE BUILD COMPLETED")
    print("=" * 60)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    try:

        build_vector_store()

    finally:

        close_client()