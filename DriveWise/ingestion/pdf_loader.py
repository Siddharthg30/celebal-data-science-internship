from pathlib import Path
import json
import re
import fitz  # PyMuPDF


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean extracted PDF text while preserving useful
    information such as numbers, units and headings.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.;:])", r"\1", text)

    return text.strip()


# --------------------------------------------------
# BRAND / MODEL DETECTION
# --------------------------------------------------

def infer_brand_model(pdf_path: Path):
    """
    Infer brand and model from the folder/file name.

    Current dataset structure:
        data/raw/Hyundai/creta.pdf
        data/raw/Hyundai/venue.pdf
        data/raw/Hyundai/verna.pdf
    """

    brand = pdf_path.parent.name
    model = pdf_path.stem.replace("_", " ").title()

    return brand, model


# --------------------------------------------------
# PDF EXTRACTION
# --------------------------------------------------

def extract_pdf(pdf_path: Path) -> dict:
    """
    Extract a PDF page-by-page while preserving
    page numbers and basic PDF metadata.
    """

    brand, model = infer_brand_model(pdf_path)

    document_id = f"{brand.lower()}_{model.lower().replace(' ', '_')}"

    pages = []

    with fitz.open(pdf_path) as document:

        pdf_metadata = document.metadata

        for page_number, page in enumerate(document, start=1):

            raw_text = page.get_text("text")

            cleaned_text = clean_text(raw_text)

            pages.append(
                {
                    "page_number": page_number,
                    "text": cleaned_text,
                    "character_count": len(cleaned_text),
                    "word_count": len(cleaned_text.split()),
                }
            )

        result = {
            "document_id": document_id,
            "brand": brand,
            "model": model,
            "document_type": "brochure",
            "source_file": pdf_path.name,
            "source_path": str(pdf_path.relative_to(BASE_DIR)),
            "page_count": len(document),
            "pdf_metadata": pdf_metadata,
            "pages": pages,
        }

    return result


# --------------------------------------------------
# SAVE PROCESSED DOCUMENT
# --------------------------------------------------

def save_processed_document(document: dict, pdf_path: Path):

    output_file = PROCESSED_DIR / f"{pdf_path.stem}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            document,
            file,
            indent=2,
            ensure_ascii=False
        )

    return output_file


# --------------------------------------------------
# PROCESS ALL BROCHURES
# --------------------------------------------------

def process_all_pdfs():

    pdf_files = sorted(RAW_DIR.rglob("*.pdf"))

    if not pdf_files:
        print("❌ No PDF files found.")
        print(f"Expected PDFs inside: {RAW_DIR}")
        return

    print("=" * 60)
    print("DRIVE WISE - PDF INGESTION")
    print("=" * 60)

    print(f"Found {len(pdf_files)} PDF files\n")

    for pdf_path in pdf_files:

        print(f"Processing: {pdf_path.name}")

        try:
            document = extract_pdf(pdf_path)

            output_file = save_processed_document(
                document,
                pdf_path
            )

            print(
                f"✓ {document['brand']} {document['model']}"
                f" | Pages: {document['page_count']}"
            )

            print(f"  Saved: {output_file}\n")

        except Exception as error:

            print(f"❌ Failed: {pdf_path.name}")
            print(f"   Error: {error}\n")

    print("=" * 60)
    print("INGESTION COMPLETED")
    print("=" * 60)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    process_all_pdfs()