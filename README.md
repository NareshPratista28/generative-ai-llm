# 🚀 Generative AI LLM for Java Programming Questions

A system that automatically generates Java programming questions for educational purposes using Large Language Models (LLMs), enhanced with Retrieval-Augmented Generation (RAG).

---

## 📦 Features

- Automatically generates Java questions based on provided materials
- Uses local LLMs like Ollama
- Enhanced with RAG for more relevant question generation
- FastAPI-based backend server

---

## 🔧 Prerequisites

Make sure you have the following installed:

- Python 3.8 or higher
- Ollama (locally installed or accessible via API)
- Required Python packages listed in `requirements.txt`

---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/generative-ai-llm.git
cd generative-ai-llm
```

2. **Create a Virtual Environment:**

```bash
python -m venv env
source env/bin/activate      # For Linux/macOS
env\Scripts\activate         # For Windows
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Build the Vector Store:**

```bash
python build_vector_store.py
```

5. **Start the Server:**

```bash
uvicorn main:app --reload
```
