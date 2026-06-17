# 📄 PDF Intelligence Assistant

PDF Intelligence Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload one or multiple PDF documents and ask questions in natural language.

The system extracts information from PDFs, retrieves the most relevant content using semantic search, and generates grounded answers using Gemini.

---

## ✨ Key Features

### 📂 Document Processing

- Upload multiple PDF documents
- Docling-powered PDF parsing
- Heading-aware document chunking
- Support for large academic and reference PDFs

### 🔎 Intelligent Retrieval

- BGE-M3 embeddings
- FAISS vector search
- Semantic similarity retrieval
- Source-grounded responses

### 🧠 Answer Generation

- Powered by Gemini 2.5 Flash
- Structured answers
- Comparison tables when required
- Summaries and study notes
- Context-aware explanations

### 🎨 User Experience

- Clean and responsive Streamlit interface
- Suggested question prompts
- Expandable source references
- Multi-document question answering

---

## ⚙️ Tech Stack

| Layer | Technology |
|---------|------------|
| PDF Parsing | Docling |
| Chunking | Heading-Aware Chunking |
| Embeddings | BGE-M3 |
| Vector Search | FAISS |
| LLM | Gemini 2.5 Flash |
| Frontend | Streamlit |

---

## 🏗️ System Architecture

```text
PDF Upload
     │
     ▼
Docling Parser
     │
     ▼
Heading-Aware Chunking
     │
     ▼
BGE-M3 Embeddings
     │
     ▼
FAISS Vector Search
     │
     ▼
Relevant Context Retrieval
     │
     ▼
Gemini 2.5 Flash
     │
     ▼
Grounded Answer Generation
```

---

## 📁 Project Structure

```text
pdf-intelligence-assistant
│
├── app.py
│
├── src
│   ├── parser.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── llm.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pdf-intelligence-assistant.git

cd pdf-intelligence-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the Application

```bash
streamlit run app.py
```

---

## 💬 Example Questions

### 📖 Understanding Concepts

```text
What are the different types of emergencies?
```

### 📝 Summarization

```text
Summarize the uploaded document.
```

### 📊 Comparison

```text
State 5 differences between public and private companies.
```

### 🎓 Study Notes

```text
Create concise study notes from this document.
```

---

## 🎯 Use Cases

- Student Learning Assistant
- Exam Preparation
- Research Paper Exploration
- Legal & Policy Document Analysis
- Knowledge Base Search
- Academic Revision Tool

---

## 🔮 Future Enhancements

- OCR Support for Scanned PDFs
- BGE Reranker Integration
- Page-Level Citations
- Answer Export (PDF/DOCX)
- Conversation Memory
- Hybrid Retrieval Pipeline

---

## 👩‍💻 Author

**Ridhima Garg**

B.Tech Computer Science Engineering

Interested in AI Applications, RAG Systems, LLMs and Full-Stack Development.

---

Built using **Docling**, **BGE-M3**, **FAISS** and **Gemini 2.5 Flash**.
