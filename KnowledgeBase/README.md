
# 📘 Contributor README: RAG 系統開發與優化平台

## 🧭 Project Overview

This platform enables modular development and optimization of Retrieval-Augmented Generation (RAG) systems. It supports document ingestion, vector indexing, retrieval strategies, generative model integration, and evaluation pipelines.

---

## 🧱 Core Modules

| Module | Path | Description |
|--------|------|-------------|
| Document Loader | `loader/` | Parses and cleans input documents |
| Vector Indexing | `indexing/` | Embeds and stores documents in vector DB |
| Retriever Engine | `retriever/` | Implements dense/sparse retrieval |
| RAG Core | `rag_core/` | Combines retrieval with generation |
| Prompt Manager | `prompts/` | Manages prompt templates and chaining |
| Evaluation Suite | `eval/` | Benchmarks output quality |
| Optimization Engine | `trainer/` | Fine-tunes retriever/generator |
| API Layer | `api/` | RESTful endpoints for interaction |
| Dashboard | `dashboard/` | Web UI for experimentation |
| Model Registry | `registry/` | Stores model versions and metadata |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/rag-platform.git
cd rag-platform
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch development server

```bash
uvicorn api.main:app --reload
```

### 4. Access dashboard

Visit `http://localhost:8000/dashboard`

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🧠 Contributing Guidelines

- Follow module boundaries and interface contracts.
- Document new components in `/docs/`.
- Use `config/experiments/` for reproducible setups.
- Submit PRs with test coverage and sample usage.

---

## 📂 Directory Structure

```plaintext
rag-platform/
├── loader/
├── indexing/
├── retriever/
├── rag_core/
├── prompts/
├── eval/
├── trainer/
├── api/
├── dashboard/
├── registry/
├── config/
├── tests/
└── docs/
```

---

# 🧾 Sample Config File: `config/experiments/rag_default.yaml`

```yaml
experiment_name: "baseline_rag_test"
retriever:
  type: "dense"
  model: "sentence-transformers/all-MiniLM-L6-v2"
  top_k: 5
generator:
  model: "meta-llama/Llama-2-7b-chat"
  temperature: 0.7
  max_tokens: 512
documents:
  source: "data/corpus/"
  format: ["pdf", "md", "html"]
embedding:
  batch_size: 32
  normalize: true
evaluation:
  metrics: ["BLEU", "ROUGE", "factuality"]
  test_set: "data/test_queries.json"
logging:
  level: "INFO"
  output_dir: "logs/baseline_rag_test/"
```
