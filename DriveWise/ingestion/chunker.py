from pathlib import Path
import json
import re

from section_detector import detect_section


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

CHUNK_DIR = PROCESSED_DIR / "chunks"

CHUNK_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MAX_CHUNK_WORDS = 250
OVERLAP_WORDS = 40


# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------

def normalize_text(text: str) -> str:

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# SPLIT LARGE TEXT
# --------------------------------------------------

def split_text(text: str):

    words = text.split()

    if len(words) <= MAX_CHUNK_WORDS:
        return [text]

    chunks = []

    start = 0

    while start < len(words):

        end = start + MAX_CHUNK_WORDS

        chunk_words = words[start:end]

        chunks.append(" ".join(chunk_words))

        if end >= len(words):
            break

        start = end - OVERLAP_WORDS

    return chunks


# --------------------------------------------------
# CREATE CHUNKS FOR ONE DOCUMENT
# --------------------------------------------------

def create_chunks(document: dict):

    chunks = []

    brand = document["brand"]
    model = document["model"]
    document_id = document["document_id"]
    source_file = document["source_file"]

    for page in document["pages"]:

        page_number = page["page_number"]

        text = normalize_text(page["text"])

        # Ignore completely empty pages
        if not text:
            continue

        section = detect_section(text)

        page_chunks = split_text(text)

        for chunk_index, chunk_text in enumerate(
            page_chunks,
            start=1
        ):

            chunk_id = (
                f"{brand.upper()}_"
                f"{model.upper()}_"
                f"{section.upper()}_"
                f"P{page_number}_"
                f"C{chunk_index}"
            )

            chunk = {

                "chunk_id": chunk_id,

                "text": chunk_text,

                "metadata": {

                    "document_id": document_id,

                    "brand": brand,

                    "model": model,

                    "document_type":
                        document["document_type"],

                    "source_file":
                        source_file,

                    "page_number":
                        page_number,

                    "section":
                        section,

                    "chunk_index":
                        chunk_index,

                    "word_count":
                        len(chunk_text.split())
                }
            }

            chunks.append(chunk)

    return chunks


# --------------------------------------------------
# PROCESS ONE JSON DOCUMENT
# --------------------------------------------------

def process_document(json_path: Path):

    with open(
        json_path,
        "r",
        encoding="utf-8"
    ) as file:

        document = json.load(file)

    chunks = create_chunks(document)

    output = {

        "document_id":
            document["document_id"],

        "brand":
            document["brand"],

        "model":
            document["model"],

        "source_file":
            document["source_file"],

        "chunk_count":
            len(chunks),

        "chunks":
            chunks
    }

    output_path = (
        CHUNK_DIR /
        f"{json_path.stem}_chunks.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    return output_path, len(chunks)


# --------------------------------------------------
# PROCESS ALL DOCUMENTS
# --------------------------------------------------

def process_all_documents():

    json_files = sorted(
        PROCESSED_DIR.glob("*.json")
    )

    # Prevent processing already-generated chunk files
    json_files = [
        file for file in json_files
        if file.parent.name == "processed"
    ]

    if not json_files:

        print("No processed JSON files found.")

        return

    print("=" * 60)
    print("DRIVE WISE - STRUCTURED CHUNKING")
    print("=" * 60)

    for json_file in json_files:

        print(f"\nProcessing: {json_file.name}")

        try:

            output_path, count = process_document(
                json_file
            )

            print(
                f"✓ Created {count} chunks"
            )

            print(
                f"  Saved: {output_path}"
            )

        except Exception as error:

            print(
                f"❌ Failed: {json_file.name}"
            )

            print(
                f"   Error: {error}"
            )

    print("\n" + "=" * 60)
    print("CHUNKING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    process_all_documents()