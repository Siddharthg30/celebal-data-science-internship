# DriveWise — AI-Powered Vehicle Information Assistant

DriveWise is a Retrieval-Augmented Generation (RAG) based vehicle information assistant.

It allows users to ask questions about a specific vehicle and retrieves relevant information from vehicle documentation using semantic vector search and a cross-encoder reranker. When enabled, Google Gemini generates a grounded response using only the retrieved document context.

The application is implemented using Python, Flask, Qdrant, Sentence Transformers, Cross-Encoder reranking, and Google Gemini.

---

## 1. Project Overview

Vehicle brochures and specification documents contain information across multiple sections such as:

- Safety
- Performance
- Interior
- Exterior
- Connectivity
- Colours
- ADAS-related features

Finding specific information manually can be time-consuming.

DriveWise provides a conversational interface where users can select a vehicle and ask questions about it.

The system:

1. Receives the user's question.
2. Applies vehicle metadata filtering.
3. Retrieves relevant document chunks from Qdrant.
4. Reranks the retrieved chunks using a Cross-Encoder.
5. Applies a relevance threshold.
6. Sends relevant context to Gemini when generation is enabled.
7. Returns a grounded answer and source information.
8. Rejects questions that are insufficiently related to the available vehicle documents.

---

## 2. Key Features

### Vehicle-specific querying

Users can select:

- Brand
- Model

and ask questions about the selected vehicle.

### Semantic retrieval

The system uses:

`all-MiniLM-L6-v2`

to convert both document chunks and user queries into embeddings.

### Metadata filtering

Qdrant retrieval can filter results using:

- Brand
- Model

This helps prevent information from other vehicles from being retrieved.

### Cross-Encoder reranking

Retrieved candidates are reranked using:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

The system initially retrieves up to 10 candidates and reranks them before generation.

### Relevance filtering

A relevance threshold is used to reject queries when the retrieved information is insufficiently relevant.

This helps prevent DriveWise from answering unrelated questions using irrelevant vehicle information.

### Grounded generation

When Gemini is enabled, the generation prompt instructs the model to:

- Use only the supplied vehicle-document context.
- Avoid outside knowledge.
- Avoid inventing vehicle specifications.
- Preserve variant-specific information.
- Include page citations for factual claims.

### Source information

Responses can include:

- Chunk ID
- Model
- Section
- Page number
- Source file
- Reranker score

### Gemini fallback

If Gemini is disabled or unavailable, DriveWise falls back to the most relevant retrieved document context instead of completely failing.

### Health check API

The application provides:

`GET /api/health`

which reports the service health and whether Gemini generation is enabled.

---

# 3. System Architecture

```text
                         USER
                           |
                           v
                +----------------------+
                |    Flask Frontend    |
                |  HTML / CSS / JS     |
                +----------+-----------+
                           |
                           v
                    POST /api/chat
                           |
                           v
                +----------------------+
                | Query + Brand + Model|
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Query Embedding      |
                | all-MiniLM-L6-v2     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Qdrant Vector Search |
                | Top 10 Candidates    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Cross-Encoder        |
                | Reranker             |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Relevance Threshold  |
                +----------+-----------+
                           |
                    +------+------+
                    |             |
                 Relevant      Irrelevant
                    |             |
                    v             v
             +-------------+   Reject
             |   Gemini    |
             | 2.5 Flash   |
             +------+------+ 
                    |
                    v
             Grounded Answer
                    |
                    v
             Sources + Pages
                    |
                    v
                  USER

# 4. Project Structure

DriveWise/
│
├── app.py
│
├── retrieval/
│   ├── __init__.py
│   ├── retriever.py
│   ├── reranker.py
│   └── vector_store.py
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
├── data/
│   ├── raw/
│   ├── processed/
│   │   └── chunks/
│   └── qdrant/
│
├── tests/
│   └── test_questions.py
│
├── requirements.txt
├── .gitignore
└── README.md