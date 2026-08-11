import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

USE_GEMINI = os.getenv(
    "USE_GEMINI",
    "true"
).lower() == "true"

MAX_CONTEXT_RESULTS = 5
MAX_TEXT_PER_RESULT = 1800

# Gemini generation configuration
TEMPERATURE = 0.1
MAX_OUTPUT_TOKENS = 1500


# ============================================================
# API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠ GEMINI_API_KEY is not configured.")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = None

if USE_GEMINI and GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    print(
        f"Gemini generation enabled: {MODEL_NAME}"
    )

else:

    print(
        "Gemini generation disabled."
    )


# ============================================================
# CONTEXT BUILDER
# ============================================================

def build_context(
    results: List[Dict[str, Any]]
) -> str:

    """
    Convert reranked retrieval results into
    structured context for Gemini.
    """

    if not results:
        return ""

    context_blocks = []

    for index, result in enumerate(
        results[:MAX_CONTEXT_RESULTS],
        start=1
    ):

        text = (
            result.get("text")
            or ""
        ).strip()

        if not text:
            continue

        text = text[:MAX_TEXT_PER_RESULT]

        model = result.get(
            "model",
            "Unknown"
        )

        section = result.get(
            "section",
            "Unknown"
        )

        page = result.get(
            "page_number",
            "Unknown"
        )

        source_file = result.get(
            "source_file",
            "Unknown"
        )

        chunk_id = result.get(
            "chunk_id",
            "Unknown"
        )

        block = f"""
SOURCE {index}

Model: {model}
Section: {section}
Page: {page}
Source File: {source_file}
Chunk ID: {chunk_id}

Content:
{text}
""".strip()

        context_blocks.append(block)

    return "\n\n".join(
        context_blocks
    )


# ============================================================
# SYSTEM INSTRUCTIONS
# ============================================================

SYSTEM_PROMPT = """
You are DriveWise, a vehicle information assistant.

Your job is to answer the user's question using ONLY
the vehicle-document context provided to you.

GROUNDING RULES:

1. Use only information explicitly supported by the
   provided context.

2. Never use outside knowledge.

3. Never invent vehicle specifications, prices, mileage,
   features, variants, availability, or technical details.

4. If the requested information is not present in the
   provided context, say:

   "The requested information could not be found in the
   provided vehicle documents."

5. Do not assume that a feature is standard merely because
   it appears in the document.

6. Preserve variant-specific information.

7. If a feature is available only on certain variants,
   mention those variants.

8. Distinguish carefully between:

   - standard features
   - available features
   - variant-specific features
   - optional features
   - ADAS features

9. Combine duplicate information from multiple sources
   instead of unnecessarily repeating it.

10. Do not cite a source unless it actually supports
    the statement.

CITATIONS:

Every factual statement derived from the documents should
include a page citation.

Use:

[Page 8]

For multiple pages:

[Pages 8, 15]

When useful, include the section:

[Safety, Page 8]

ANSWER STYLE:

- Answer the question directly.
- Be concise and professional.
- Use headings when useful.
- Use bullet points for feature lists.
- Preserve important variant information.
- Do not reproduce large sections of the documents.
- Do not mention Qdrant, embeddings, chunks, retrieval,
  reranking, or internal RAG implementation details.
"""


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(
    query: str,
    context: str
) -> str:

    return f"""
{SYSTEM_PROMPT}

USER QUESTION:

{query}

VEHICLE DOCUMENT CONTEXT:

{context}

FINAL ANSWER:

Answer the user's question using only the vehicle
document context above.

Include page citations for factual claims.
""".strip()


# ============================================================
# SAFE FALLBACK
# ============================================================

def fallback_response(
    results: List[Dict[str, Any]]
) -> str:

    """
    User-friendly fallback when Gemini is unavailable.

    We intentionally do not dump the complete retrieved
    document chunks into the UI.
    """

    if not results:

        return (
            "The requested information could not be found "
            "in the provided vehicle documents."
        )

    # Use the strongest retrieved result as a minimal
    # fallback instead of exposing large raw chunks.

    best_result = results[0]

    text = (
        best_result.get("text")
        or ""
    ).strip()

    section = best_result.get(
        "section",
        "Document"
    )

    page = best_result.get(
        "page_number",
        "Unknown"
    )

    if not text:

        return (
            "The requested information could not be generated "
            "from the available vehicle documents."
        )

    # Keep fallback concise.
    text = text[:1000]

    return (
        "Gemini is temporarily unavailable. "
        "Here is the most relevant information found "
        "in the vehicle documents:\n\n"
        f"{text}\n\n"
        f"[{section}, Page {page}]"
    )


# ============================================================
# GEMINI GENERATION
# ============================================================

def generate_answer(
    query: str,
    results: List[Dict[str, Any]]
) -> str:

    """
    Generate a grounded answer using Gemini.

    Parameters
    ----------
    query:
        User's question.

    results:
        Reranked retrieval results.

    Returns
    -------
    str
        Grounded answer or safe fallback.
    """

    # --------------------------------------------------------
    # VALIDATE QUERY
    # --------------------------------------------------------

    if not query or not query.strip():

        return (
            "Please provide a question."
        )

    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if not results:

        return (
            "The requested information could not be found "
            "in the provided vehicle documents."
        )

    # --------------------------------------------------------
    # GEMINI DISABLED
    # --------------------------------------------------------

    if not USE_GEMINI:

        print(
            "\nGemini disabled."
        )

        return fallback_response(
            results
        )

    # --------------------------------------------------------
    # CLIENT UNAVAILABLE
    # --------------------------------------------------------

    if client is None:

        print(
            "\n⚠ Gemini client unavailable."
        )

        return fallback_response(
            results
        )

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context = build_context(
        results
    )

    if not context:

        return (
            "The requested information could not be found "
            "in the provided vehicle documents."
        )

    # --------------------------------------------------------
    # BUILD PROMPT
    # --------------------------------------------------------

    prompt = build_prompt(
        query=query,
        context=context
    )

    # --------------------------------------------------------
    # GEMINI REQUEST
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=TEMPERATURE,

                max_output_tokens=MAX_OUTPUT_TOKENS,

                response_mime_type="text/plain"
            )
        )

        answer = (
            response.text
            if response
            else None
        )

        # ----------------------------------------------------
        # EMPTY RESPONSE
        # ----------------------------------------------------

        if not answer or not answer.strip():

            print(
                "\n⚠ Gemini returned an empty response."
            )

            return fallback_response(
                results
            )

        return answer.strip()

    # --------------------------------------------------------
    # GEMINI ERROR
    # --------------------------------------------------------

    except Exception as e:

        error_message = str(e)

        print(
            f"\n⚠ Gemini generation failed: {error_message}"
        )

        # Keep the API alive even when Gemini is unavailable.
        print(
            "Falling back to document context."
        )

        return fallback_response(
            results
        )