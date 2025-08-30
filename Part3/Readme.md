# Part 3 – Streamlit UI (GitLab Chatbot)

This module provides a **Streamlit-based web interface** for interacting with the GitLab Handbook & Product Direction chatbot. It builds on **Part 2 (LLM Integration)** by adding a polished frontend where users can ask questions, view answers, and inspect supporting source documents.

---

## 📂 Project Structure

```
Part1/
└── data/
└── faiss_index/ # Pre-built FAISS vector store (from Part 1)
Part2/
└── llm_integration.py # Backend: Retrieval + Gemini LLM integration
Part3/
├── .streamlit/
│ └── secrets.toml # Secure API key storage (ignored in Git)
├── Code_snippets_explanation.md # Notes & breakdown of important code snippets
├── Readme.md # Documentation for Part 3
└── streamlit_app.py # Frontend: Streamlit chatbot UI
```

- **Part1**: Data collection & FAISS index creation  
- **Part2**: LLM integration (retrieval + Gemini model)  
- **Part3**: Streamlit frontend for an interactive chatbot  

---

## ⚙️ Features

- **🔑 Secure API Key Handling** – Reads API key from Streamlit `secrets.toml`.
- **🤖 Conversational Q&A** – Uses Part 2’s `build_qa_chain()` for context-aware answers.
- **🖼️ Modern Chat UI** – Built with `st.chat_input` and `st.chat_message`:
  - User + Assistant avatars
  - Persistent chat history
- **📚 Source Transparency** – Expandable section shows source documents and context.
- **✨ GitLab-specific Training** – Only answers from Handbook & Product Direction.

---

## 🔧 Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure secrets**

   In `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "your_google_api_key_here"
   ```

3. **Ensure FAISS index exists** (from Part 1):
   ```
   Part1/data/faiss_index/
   ```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run Part3/streamlit_app.py
```

Then open the link in your browser (default: `http://localhost:8501`).

---

## 🖼️ Example UI

- **Welcome message** explains supported GitLab resources.  
- **Chat Input** allows freeform questions.  
- **Chat History** persists across messages in session.  
- **Expandable "📚 Sources & Reasoning"** shows retrieved documents with metadata.

---

## 📜 Customization

- **Change title & description**
  ```python
  st.title("🤖 GitLab Handbook & Direction AI Chatbot")
  st.markdown("Welcome! This GenAI assistant helps...")
  ```

- **Modify chat avatars**
  ```python
  with st.chat_message("user", avatar="🧑"):
  with st.chat_message("assistant", avatar="🤖"):
  ```

- **Change source formatting**
  In the expander section, adjust how metadata and text snippets are displayed.

---

## 🚀 Workflow Recap

- ✅ Part 1: FAISS Index (data preparation)  
- ✅ Part 2: LLM Integration (retriever + Gemini chain)  
- ✅ Part 3: Streamlit UI (frontend)  

---

## 📌 Notes

- Requires **Gemini API key** in Streamlit secrets.  
- Chatbot will **decline off-topic questions politely**.  
- Best performance with **Gemini 1.5 Flash** for low-latency answers.  

---

## 🏷 License

This project is for **educational purposes** and references GitLab’s public documentation.