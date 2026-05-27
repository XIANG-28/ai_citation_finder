# 🧠 AI Medical Evidence Finder

An AI-powered biomedical search engine that transforms natural language clinical descriptions into PubMed-backed scientific evidence with sentence-level citation grounding.

---

## 🚀 Live Demo

- 🔗 Frontend (Streamlit): https://aicitationfinder.streamlit.app/
- 🔗 Backend API (FastAPI): https://ai-citation-finder.onrender.com
- 📘 API Docs: https://ai-citation-finder.onrender.com/docs

---

## 📌 Problem Statement

Medical literature search is often:

- Keyword-based and not semantic
- Time-consuming for clinicians and researchers
- Difficult to extract directly citable evidence
- Not optimized for natural language queries

This project aims to bridge the gap between **clinical language → scientific evidence**.

---

## 💡 Solution

This system converts free-form clinical input into structured PubMed evidence using an AI-driven pipeline:

- LLM-based query expansion (GPT-4o-mini)
- Multi-query PubMed retrieval (E-utilities API)
- Deduplication and result merging
- Semantic ranking using OpenAI embeddings
- Sentence-level evidence extraction

---


---

## 🧠 System Architecture

```
User Input (Clinical Sentence)
        ↓
LLM Query Expansion (GPT-4o-mini)
        ↓
Multi-query PubMed Retrieval (ESearch API)
        ↓
Deduplication of PMIDs
        ↓
Fetch Abstracts (EFetch XML)
        ↓
Sentence Segmentation
        ↓
Embedding-based Semantic Ranking
        ↓
Hybrid Scoring (Sentence + Document)
        ↓
Final Ranked Evidence List
        ↓
Streamlit UI (User-friendly Citation Display)
```


---

## ⚙️ Tech Stack

**Backend**
- FastAPI
- PubMed E-utilities API
- XML parsing
- OpenAI API

**AI / NLP**
- GPT-4o-mini (query expansion)
- text-embedding-3-small (semantic similarity)
- Cosine similarity ranking

**Frontend**
- Streamlit

**Deployment**
- Render (FastAPI backend)
- Streamlit Cloud / Render (frontend)

---

## 🔍 Key Features

### 🧠 AI Query Understanding
Transforms clinical sentences into optimized PubMed search queries using LLM.

### 📚 Multi-Query Retrieval Strategy
Generates multiple keyword combinations to maximize recall in PubMed.

### 📊 Hybrid Ranking System
Combines:
- Document-level embedding similarity
- Sentence-level semantic matching

### ✂️ Evidence Extraction
Extracts the most relevant sentence from abstracts for citation purposes.

### 🌐 End-to-End Web App
Fully deployed system with real-time search and visualization.

---

## 🧪 Example

### Input
key words or sentences

### Output
- PubMed papers ranked by relevance
- Highlighted evidence sentence from abstract
- Direct PubMed links for citation

---

## 🧱 API Usage

### POST /search

Search PubMed for biomedical evidence based on a clinical sentence.

---

#### 📌 Request

- Method: `POST`
- Endpoint: `/search`
- Content-Type: `application/json`

```json
{
  "query": "Acupuncture reduces hot flashes via neuroendocrine regulation"
}
```
## 📈 Technical Highlights

- Multi-stage retrieval pipeline:
  (Query → Document → Sentence)

- Hybrid ranking system:
  keyword relevance + embedding similarity

- Robust PubMed API integration with deduplication

- Sentence-level evidence grounding (explainable AI retrieval)

---

## 🧠 Future Improvements

- Add citation styles (APA / Vancouver)
- Highlight matched sentence in UI
- Add caching layer (Redis)
- Improve ranking with biomedical fine-tuned LLM
- Add user history & saved citations

---

## 👩‍💻 Author

Built as a full-stack AI engineering portfolio project focusing on:

- Biomedical NLP
- LLM-based search systems
- Information retrieval pipelines
- Explainable AI retrieval


```
ai_citation_finder/
│
├── backend/
│   ├── main.py                # FastAPI入口
│   ├── routes/
│   │   └── search.py          # API路由
│   ├── services/
│   │   ├── pubmed.py          # 调用PubMed API
│   │   ├── parser.py          # 解析XML
│   │   └── matcher.py         # 找最佳句子（后面会升级embedding）
│   └── models/
│       └── schemas.py         # 数据结构（可选）
│
├── frontend/
│   └── app.py                 # Streamlit界面
│
├── requirements.txt
└── README.md```