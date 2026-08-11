Absolutely. Copy everything inside the code block below and paste it directly into your `DriveWise/README.md`.

````markdown
# DriveWise — Metadata-Aware Automotive RAG Assistant

## Overview

**DriveWise** is a metadata-aware Retrieval-Augmented Generation (RAG) assistant for querying vehicle specifications and features from Hyundai vehicle brochures.

The system combines **semantic embeddings, metadata-aware retrieval, Qdrant vector search, cross-encoder reranking, relevance filtering, and Gemini-based generation** to provide grounded answers from the available vehicle documents.

DriveWise is designed to answer vehicle-related questions while rejecting queries that are not sufficiently relevant to the available vehicle documentation.

---

## Key Features

- **Metadata-aware retrieval**
  - Uses vehicle brand and model information during retrieval.
- **Semantic search**
  - Converts user queries and document chunks into semantic embeddings.
- **Qdrant vector search**
  - Performs similarity search over the indexed vehicle document chunks.
- **Cross-encoder reranking**
  - Reranks retrieved candidates based on query-document relevance.
- **Relevance threshold**
  - Rejects queries when the retrieved content is insufficiently relevant.
- **Grounded answer generation**
  - Uses Gemini to generate answers from retrieved vehicle-document context.
- **PDF-based knowledge base**
  - Vehicle information is extracted and processed from Hyundai brochures.
- **Flask REST API**
  - Provides the backend API for the application.
- **Web interface**
  - Provides an interactive interface for asking vehicle-related questions.
- **Evaluation tests**
  - Includes tests for retrieval, reranking, and RAG behavior.

---

# Architecture

```text
                    Hyundai Vehicle Brochures
                              |
                              v
                    +--------------------+
                    |    PDF Loader      |
                    |  Text Extraction   |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Section Detection  |
                    |     & Metadata     |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    |      Chunking      |
                    | Document -> Chunks  |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    |  Embedding Model   |
                    | Semantic Embeddings|
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    |      Qdrant        |
                    |   Vector Search    |
                    +---------+----------+
                              |
                         Top-K Results
                              |
                              v
                    +--------------------+
                    | Cross-Encoder      |
                    |    Reranker        |
                    +---------+----------+
                              |
                       Relevance Filter
                              |
                              v
                    +--------------------+
                    |   Gemini 2.5 Flash |
                    | Grounded Generation|
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    |     Flask API      |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    |   DriveWise UI     |
                    +--------------------+
````

---

# Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Backend              | Flask                 |
| Frontend             | HTML, CSS, JavaScript |
| PDF Processing       | PyMuPDF               |
| Embeddings           | Sentence Transformers |
| Vector Database      | Qdrant                |
| Reranking            | Cross-Encoder         |
| LLM                  | Gemini 2.5 Flash      |
| API                  | REST API              |
| Testing              | Python                |
| Version Control      | Git & GitHub          |
| Deployment           | Render                |

---

# Project Structure

```text
DriveWise/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── Hyundai/
│   │       ├── creta.pdf
│   │       ├── venue.pdf
│   │       └── verna.pdf
│   │
│   ├── processed/
│   │   ├── creta.json
│   │   ├── venue.json
│   │   ├── verna.json
│   │   │
│   │   └── chunks/
│   │       ├── creta_chunks.json
│   │       ├── venue_chunks.json
│   │       └── verna_chunks.json
│   │
│   └── metadata/
│       └── documents.json
│
├── ingestion/
│   ├── __init__.py
│   ├── pdf_loader.py
│   ├── section_detector.py
│   └── chunker.py
│
├── retrieval/
│   ├── __init__.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── reranker.py
│
├── generation/
│   ├── __init__.py
│   └── generator.py
│
├── frontend/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
└── tests/
    ├── test_questions.py
    ├── test_rag.py
    └── test_reranking.py
```

---

# How DriveWise Works

## 1. Document Ingestion

Vehicle brochures are stored as PDF files under:

```text
data/raw/Hyundai/
```

The current dataset contains brochures for:

* Hyundai Creta
* Hyundai Venue
* Hyundai Verna

The PDF loader extracts text from the vehicle brochures.

---

## 2. Section Detection and Metadata

The extracted brochure content is organized into relevant sections such as:

* Safety
* Performance
* Connectivity
* Interior
* Exterior
* ADAS
* Colours

Metadata such as the vehicle brand, model, section, and page information is retained with the document chunks.

This allows DriveWise to perform more targeted retrieval.

---

## 3. Document Chunking

Large documents are divided into smaller chunks before indexing.

A chunk can contain information such as:

```text
Brand
Model
Section
Page Number
Document
Text Content
```

This makes the documents easier to retrieve semantically.

---

## 4. Semantic Embeddings

The document chunks are converted into vector representations using a Sentence Transformer embedding model.

When a user submits a question, the query is also converted into an embedding.

This allows DriveWise to retrieve information based on semantic meaning rather than relying only on exact keyword matching.

For example:

```text
"What safety equipment is available?"
```

can retrieve content related to:

```text
Safety features
Airbags
Electronic Stability Control
ADAS
```

even if the exact words in the question do not appear in the document.

---

## 5. Metadata-Aware Qdrant Retrieval

The query is processed using the selected vehicle information.

For example:

```text
Brand: Hyundai
Model: Creta
```

The system performs vector similarity search using Qdrant.

The retrieval pipeline is:

```text
User Query
    |
    v
Query Embedding
    |
    v
Metadata Filtering
    |
    v
Qdrant Vector Search
    |
    v
Top-K Candidates
```

The current retrieval configuration uses:

```text
Top-K = 10
```

candidate results before reranking.

---

## 6. Cross-Encoder Reranking

The initial vector search retrieves candidate documents.

DriveWise then applies a cross-encoder reranker to evaluate the relevance of each query-document pair.

```text
10 Retrieved Candidates
          |
          v
    Cross-Encoder
          |
          v
5 Reranked Results
```

The reranker assigns a relevance score to each candidate.

This additional stage improves the quality of the context provided to the generation model.

---

## 7. Relevance Threshold

DriveWise includes a relevance check before answer generation.

If the highest reranker score is below the configured relevance threshold, the system considers the query insufficiently relevant and does not generate an answer from unrelated documents.

For example:

```text
Query:
What is the population of India?

Brand:
Hyundai

Model:
Creta

Top reranker score:
-11.0002

Result:
Query considered insufficiently relevant.
```

This prevents unrelated questions from being answered using irrelevant vehicle brochure content.

---

## 8. Gemini Answer Generation

If the retrieved results pass the relevance check, the relevant context is passed to Gemini.

The generation pipeline is:

```text
User Query
     |
     v
Qdrant Retrieval
     |
     v
Cross-Encoder Reranking
     |
     v
Relevance Filtering
     |
     v
Relevant Document Context
     |
     v
Gemini 2.5 Flash
     |
     v
Final Answer
```

Gemini therefore generates the response using the retrieved vehicle-document context.

---

# Example Queries

## Supported Query

```text
What safety features does the Hyundai Creta have?
```

DriveWise retrieves relevant safety information, reranks the results, and generates an answer using the retrieved brochure context.

## Another Supported Query

```text
What connectivity features does the Creta have?
```

The system retrieves and reranks relevant connectivity sections before generating the answer.

## Irrelevant Query

```text
What is the population of India?
```

The system identifies that the retrieved vehicle documentation is not relevant enough and rejects the query instead of generating an unrelated answer.

---

# API

DriveWise provides a Flask REST API.

### Chat Endpoint

```text
POST /api/chat
```

The endpoint processes the user's vehicle-related question through the complete RAG pipeline.

The application can be started locally using:

```bash
python app.py
```

The application runs on:

```text
http://127.0.0.1:5000
```

For deployment using Gunicorn:

```bash
gunicorn app:app
```

---

# Running Locally

## 1. Clone the Repository

```bash
git clone https://github.com/Siddharthg30/celebal-data-science-internship.git
```

Navigate to the DriveWise project:

```bash
cd celebal-data-science-internship/DriveWise
```

---

## 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API Key

Create a `.env` file in the project directory if required.

Example:

```env
GOOGLE_API_KEY=your_api_key
```

Do not commit API keys, credentials, or other secrets to GitHub.

---

## 5. Run the Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

# Testing

DriveWise includes test scripts for evaluating retrieval and reranking behavior.

```text
tests/
├── test_questions.py
├── test_rag.py
└── test_reranking.py
```

Example evaluation questions include:

```text
What safety features does the Hyundai Creta have?

What are the engine options of the Hyundai Creta?

What connectivity features does the Hyundai Creta offer?

What interior features are available in the Hyundai Creta?

What exterior features does the Hyundai Creta have?

What colours are available for the Hyundai Creta?

What ADAS features are available in the Hyundai Creta?

What variants of the Hyundai Creta are available?

What is the mileage of the Hyundai Creta?

What is the population of India?
```

The test pipeline evaluates retrieval and reranking behavior and demonstrates how irrelevant queries can be rejected.

---

# RAG Reliability

DriveWise uses multiple stages to improve retrieval quality and grounding.

### Metadata Filtering

The selected vehicle brand and model are considered during retrieval.

### Semantic Retrieval

Qdrant retrieves documents based on semantic similarity.

### Cross-Encoder Reranking

Retrieved candidates are reranked based on query-document relevance.

### Relevance Threshold

Low-relevance results are rejected before generation.

### Grounded Generation

Gemini receives retrieved vehicle-document context instead of relying solely on general knowledge.

Overall:

```text
Metadata Filtering
       +
Semantic Retrieval
       +
Qdrant Vector Search
       +
Cross-Encoder Reranking
       +
Relevance Threshold
       +
Grounded Gemini Generation
```

---

# Deployment

DriveWise can be deployed as a Python web service using platforms such as Render.

Production start command:

```bash
gunicorn app:app
```

When deploying from the parent GitHub repository, configure the service root directory as:

```text
DriveWise
```

The application loads embedding and reranker models during startup, so sufficient memory is required for deployment.

---

# Current Knowledge Base

The current DriveWise knowledge base contains Hyundai vehicle brochures for:

```text
Hyundai Creta
Hyundai Venue
Hyundai Verna
```

The system is designed to answer questions based on the information contained in the indexed documents.

It is not intended to function as a general-purpose automotive knowledge system outside the available document collection.

---

# Future Improvements

Possible future improvements include:

* Add more vehicle manufacturers.
* Add additional vehicle models.
* Automatically ingest newly added brochures.
* Improve source citation and document traceability.
* Add conversation history.
* Add production monitoring and logging.
* Improve model loading and deployment memory usage.
* Add automated RAG evaluation using dedicated evaluation frameworks.
* Improve retrieval and reranking evaluation datasets.

---

# End-to-End Pipeline

```text
             VEHICLE BROCHURES
                     |
                     v
             PDF TEXT EXTRACTION
                     |
                     v
            SECTION DETECTION
                     |
                     v
              DOCUMENT CHUNKING
                     |
                     v
             METADATA CREATION
                     |
                     v
            EMBEDDING GENERATION
                     |
                     v
               QDRANT INDEX
                     |
                     |
             USER QUESTION
                     |
                     v
            QUERY EMBEDDING
                     |
                     v
          METADATA-AWARE SEARCH
                     |
                     v
             TOP 10 RESULTS
                     |
                     v
          CROSS-ENCODER RERANKER
                     |
                     v
             TOP 5 RESULTS
                     |
                     v
           RELEVANCE THRESHOLD
                /          \
             PASS           FAIL
              |               |
              v               v
        RETRIEVED CONTEXT    REJECT
              |
              v
        GEMINI 2.5 FLASH
              |
              v
          FINAL ANSWER
```

---

# Project Highlights

DriveWise demonstrates an end-to-end **Retrieval-Augmented Generation architecture** for automotive document intelligence.

The project combines:

* PDF document processing
* Metadata extraction
* Semantic embeddings
* Qdrant vector database
* Metadata-aware retrieval
* Cross-encoder reranking
* Relevance thresholding
* Gemini 2.5 Flash
* Flask REST API
* Interactive frontend
* Retrieval and RAG testing

The primary focus is on **retrieval quality, relevance filtering, and grounded answer generation**.

---

# Author

**Siddharth Gupta**

B.Tech — Computer Science & Engineering
Specialization: AI/ML and Robotics

GitHub:

[https://github.com/Siddharthg30](https://github.com/Siddharthg30)

---

# Internship

Developed as part of the **Celebal Technologies Data Science Internship**.

```
```
