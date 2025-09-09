# Infrastructure and Environment Details

*(Template refs: Annex IV ¶2(e))*  

## Execution Environment

- **Programming language:** Python 3.11+  
- **Virtual environment:** created with `python -m venv .venv`  
- **Dependencies:** managed via `pip`, including:  
  - `crewai` – Flow orchestration and agent framework  
  - `langchain` – core framework for LLM applications  
  - `langchain_openai` – Azure OpenAI embeddings and chat models  
  - `langchain_core` – base types and utilities for LangChain  
  - `langchain_community` – community integrations (e.g., FAISS loaders, text splitters)  
  - `qdrant_client` – vector database client for Qdrant  
  - `python-dotenv` (`dotenv`) – environment variable management  
- **Documentation engine:** MkDocs Material (`mkdocs serve`)  
- **Documentation engine:** MkDocs Material (`mkdocs serve`)  

---

## Vector Database

- **Technology:** Qdrant (running via Docker container)  
- **Default ports:**  
  - REST API → `http://localhost:6333`  
  - gRPC → `http://localhost:6334`  
- **Storage:** Docker volume (`qdrant-storage`) bound to local project directory  
- **Collection name:** `outputs`  

---

## Cloud Services

- **Provider:** Azure OpenAI  
- **Chat model:** `gpt-4o`  
- **Embedding model:** `text-embedding-ada-002`  
- **Configuration:** managed via `.env` file with API key and endpoint  
- **Subscription:** Azure (free or enterprise depending on account)  

---

## Dataset Management

- **Local storage path:** `src/quiz_generator/dataset/`  
- **Content:** official certification PDFs (AI-900 initially)  
- **Update process:** manual download from Microsoft Learn when new versions are released  

---

## Interfaces

- **User interface:** Command-line wizard (terminal-based)  
- **Output formats:** JSON, Markdown, PDF  
- **Visualization:** Flow plot available via `quiz_flow.plot()`  

---

## Security & Access

- **Secrets management:** local `.env` file (optionally extendable to Azure Key Vault)  
- **Access control:** local developer machine; no external API exposed except Qdrant (localhost only)  
- **Network:** isolated to localhost during development  
