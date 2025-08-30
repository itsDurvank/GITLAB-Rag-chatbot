## About This README

This README walks you through the project’s 2nd part's file structure, explaining the key components, important files, and core operations that make up the project workflow.


## Project Structure (Part 2)

Part2/
├── Colab_Jupyter(ipynb)-Part2/ # Contains Jupyter notebook and execution guide for Part 2
│ ├── How-To-Run(ipynb) part2.pdf # Instructions for running Part2.ipynb in Google Colab
│ └── Part2.ipynb # Main notebook to integrate FAISS index with the chatbot
├── faiss_index.rar # Compressed FAISS index exported from Part1 for chatbot use
├── .env # Stores sensitive keys (e.g., Google Gemini API key) securely
├── llm_integration.py # Backend script that powers the chatbot using FAISS + LLM
├── Code_snippets_explanation.md # Line-by-line explanation of llm_integration.py for clarity
└── Readme.md # Documentation for Part 2 setup, execution, and testing


# Detailed Project Structure & Functionality – Part 2

This directory represents Phase 2 of the RAG chatbot project, where the FAISS index (built in Part 1) is connected to a Large Language Model (LLM) backend. This enables live question answering using GitLab’s Handbook and Direction documents as the knowledge base.


# Detailed Project Structure & Functionality – Part 2

This directory represents **Phase 2 of the RAG chatbot project**, where the FAISS index (built in Part 1) is connected to a Large Language Model (LLM) backend. This enables **live question answering** using GitLab’s Handbook and Direction documents as the knowledge base.


### Part2.ipynb  
- The primary Jupyter notebook for Part 2.  
  - Loads the FAISS index created in Part 1.  
  - Initializes the backend defined in `llm_integration.py`.  
  - Demonstrates live interaction with the chatbot, showing how document chunks are retrieved and answers are generated in real-time.  

---
## faiss_index.rar  
- A compressed copy of the FAISS vector index produced in Part 1.  
- Needs to be extracted or uploaded in Colab so the chatbot can access its knowledge base.  
- Ensures portability — users don’t need to rebuild the index if they just want to test the chatbot.  
---

## .env  
- Contains **secure environment variables**, primarily the Google Gemini API key.  
- Prevents sensitive credentials from being exposed in code.  
- Used by both `Part2.ipynb` and `llm_integration.py` during runtime.  

---
## llm_integration.py – *The Core Chatbot Backend*
This script wires together the FAISS retriever, Google Gemini LLM, and memory for contextual conversations.  

### Key components inside this file:
1. **Library Imports** – Brings in FAISS, HuggingFace embeddings, Google Gemini API, LangChain memory, prompt templates, and utility modules.  
2. **setup_api_key()** – Securely stores the Gemini API key in environment variables.  
3. **load_vector_store()** – Loads the FAISS index (`Part1/data/faiss_index`) and creates a retriever with Maximum Marginal Relevance search (`k=8`, `fetch_k=18`) to get diverse, non-redundant context chunks.  
4. **build_qa_chain()** –  
   - Initializes Gemini 1.5 Flash model (`temperature=0.3` for balanced factual/creative responses).  
   - Sets up **ConversationSummaryBufferMemory** to summarize past conversations, preventing token overflow.  
   - Defines a **custom PromptTemplate** to keep responses grounded in GitLab docs and well-formatted.  
   - Builds a **ConversationalRetrievalChain** combining LLM, retriever, memory, and custom prompt.  
5. **Terminal Mode (__main__ block)** –  
   - Prompts user securely for API key using `getpass`.  
   - Builds the QA chain and starts an interactive terminal chatbot.  
   - Handles errors gracefully (e.g., missing API key, retriever issues).  

This file allows **seamless reuse**:  
- In **Colab/Streamlit**, it can be imported as a module without running terminal mode.  
- In **terminal mode**, it runs standalone as a command-line chatbot.  

---
## Code_snippets_explanation.md  
- Provides a **human-readable breakdown of llm_integration.py**, explaining every function, setting, and parameter.  
- Useful for developers maintaining or extending the chatbot backend.  
- Covers:  
  - Why Gemini 1.5 Flash was chosen  
  - What each retriever/search setting means  
  - How memory works to maintain context  
  - How prompts enforce chatbot accuracy and format  
---

## Readme.md  
- Documentation specifically for **Part 2**.  
- Describes:  
  - How to set up the Colab environment  
  - Where to place `faiss_index.rar`  
  - How to load and run the chatbot in both terminal and notebook modes  
  - Any additional configuration required (like `.env` variables)  
