# 📄 Document Question Answering System using Retrieval-Augmented Generation (RAG)

## 📌 Overview

This project implements a simple **Retrieval-Augmented Generation (RAG)** system that answers questions from a custom PDF document.

Instead of relying only on a language model's internal knowledge, the system first retrieves the most relevant information from the uploaded document and then uses that context to generate an answer. This makes the responses more accurate and relevant to the document.

---

## 🎯 Objectives

* Understand the concept of Retrieval-Augmented Generation (RAG)
* Build a document-based question answering system
* Learn how embeddings and vector databases work
* Generate answers using retrieved document context
* Gain hands-on experience with Generative AI concepts

---

## ⚙️ Technologies Used

* Python
* PyPDF2
* Sentence Transformers
* FAISS
* Hugging Face Transformers
* Google FLAN-T5
* NumPy
* LangChain Text Splitters

---

## 🏗️ System Architecture

```text
                    DOCUMENT INDEXING

        PDF
         │
         ▼
   Extract Text
         │
         ▼
   Text Chunking
         │
         ▼
 Generate Embeddings
         │
         ▼
   Store in FAISS
──────────────────────────────────────────────

              QUESTION ANSWERING

      User Question
            │
            ▼
 Generate Query Embedding
            │
            ▼
     Search FAISS Index
            │
            ▼
 Retrieve Top-k Chunks
            │
            ▼
 Build Prompt (Context + Question)
            │
            ▼
         FLAN-T5
            │
            ▼
       Final Answer
```

---

## 📂 Project Structure

```text
Document-QA-RAG/
│
├── Document_QA_RAG.ipynb
├── README.md
├── requirements.txt
└── data/
    └── resume.pdf
```

---

## 🔄 Workflow

1. Load the PDF document.
2. Extract text from all pages.
3. Split the text into smaller chunks.
4. Generate embeddings for each chunk using Sentence Transformers.
5. Store the embeddings in a FAISS vector database.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant text chunks.
8. Provide the retrieved context to FLAN-T5.
9. Generate the final answer.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Document-QA-RAG.git

cd Document-QA-RAG
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

1. Place your PDF inside the `data` folder.

Example:

```text
data/
    resume.pdf
```

2. Open the notebook:

```
Document_QA_RAG.ipynb
```

3. Run all cells in order.

4. Ask questions using:

```python
ask_question("What programming languages are mentioned?")
```

---

## 💡 Example Questions

* What programming languages are mentioned?
* What technical skills are listed?
* Who is the author?
* What projects are described?
* What are the achievements?
* Which databases are used?

---

## 📈 Sample Output

**Question**

```text
What programming languages are mentioned?
```

**Answer**

```text
Java, Python, JavaScript, C, SQL, R, HTML, CSS
```

---

## 📚 Key Concepts Learned

* Retrieval-Augmented Generation (RAG)
* Text Chunking
* Sentence Embeddings
* Vector Databases
* Similarity Search
* Prompt Engineering
* Document Question Answering

---

## 🔮 Future Improvements

* Support multiple PDF documents
* Add a Streamlit web interface
* Use larger embedding models
* Integrate vector databases like Pinecone or ChromaDB
* Add conversation memory
* Deploy the project on the cloud

---

## ✅ Conclusion

This project demonstrates a simple implementation of a Retrieval-Augmented Generation (RAG) system for document question answering. It combines document retrieval with a language model to generate responses based on the document instead of relying only on the model's knowledge. This approach improves the accuracy and reliability of answers and provides a strong foundation for building more advanced AI-powered knowledge assistants.

---

## 👨‍💻 Author

**Siddharth Gupta**

B.Tech CSE (AI, ML & Robotics)

DIT University
