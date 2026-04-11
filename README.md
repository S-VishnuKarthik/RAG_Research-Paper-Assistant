

# 📄 Smart Research Paper Assistant (RAG)

## 🚀 Overview

An advanced **Retrieval-Augmented Generation (RAG)** system designed to analyze and interact with multiple research papers.
The system enables users to upload PDFs and ask intelligent questions such as summarization, comparison, and factual queries with **citation-based responses**.

---
<img width="1895" height="886" alt="Screenshot 2026-04-10 213337" src="https://github.com/user-attachments/assets/4cd5a451-4cfe-4823-a5a8-4c02521be58e" />
## 🔥 Key Features

* 📚 Multi-PDF ingestion and processing
* ⚡ Hybrid retrieval (**FAISS + BM25**)
* 🎯 Cross-encoder re-ranking for high accuracy
* 🧠 Query classification:

  * Summary
  * Comparison
  * Factual
* 📌 Citation-based answers (source + page)
* 🌐 Interactive **Streamlit UI**
* 🔍 Semantic + keyword search combined

---

## 🛠️ Tech Stack

| Layer          | Technology            |
| -------------- | --------------------- |
| Language       | Python                |
| Vector Search  | FAISS                 |
| Keyword Search | BM25                  |
| Embeddings     | Sentence Transformers |
| Re-ranking     | Cross-Encoder         |
| LLM            | OpenAI GPT            |
| UI             | Streamlit             |

---

## 🏗️ Architecture

```
          PDF Upload
             ↓
    Text Extraction (PyMuPDF)
             ↓
Chunking + Metadata (page, source, section)
             ↓
Embeddings (Sentence Transformers)
             ↓
          Indexing:
             ├── FAISS (Semantic Search)
             └── BM25 (Keyword Search)
             ↓
      Hybrid Retrieval
             ↓
    Re-ranking (Cross-Encoder)
             ↓
     Query Classification
             ↓
          LLM (Answer Generation)
             ↓
Final Output (Answer + Citations)
```

---

## 🔄 System Workflow

### Step-by-Step Flow

1. 📥 User uploads research papers (PDFs)
2. 📄 Text is extracted from each page
3. ✂️ Text is split into chunks with metadata
4. 🧠 Embeddings are generated for semantic understanding
5. ⚡ Data is indexed using:

   * FAISS (semantic similarity)
   * BM25 (keyword matching)
6. ❓ User enters a query
7. 🧠 Query is classified:

   * Summary / Comparison / Factual
8. 🔍 Hybrid retrieval fetches relevant chunks
9. 🎯 Re-ranking improves result accuracy
10. 🤖 LLM generates final answer
11. 📌 Output includes citations (paper + page)

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
HF_TOKEN=your_token_here
```

### 3️⃣ Run the app

```bash
python -m streamlit run app/streamlit_app.py
```

---

## 📌 Example Queries

* Summarize the paper
* Compare methodologies across papers
* What model is used in the research?
* What are the key findings?

---

## 📂 Project Structure

```
pdf_rag_advanced/
│
├── ingestion/
├── embeddings/
├── indexing/
├── retrieval/
├── query/
├── llm/
├── app/
├── config/
├── utils/
├── main.py
```

---

## 🔐 Security Practices

* API keys stored using `.env`
* `.env` excluded via `.gitignore`
* No secrets exposed in repository

---

## 💡 Future Improvements

* HNSW-based vector indexing
* Multi-modal RAG (images + tables)
* RAG evaluation metrics (RAGAS)
* Chat history memory
* Deployment (Docker / Cloud)

---

## 👨‍💻 Author

**Vishnu**

---
