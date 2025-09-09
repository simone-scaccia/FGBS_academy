# Integration with External Systems

*(Template refs: Annex IV ¶2(f))*  

## Overview

The Quiz Generator (CrewAI) integrates with two main external systems:  
1. **Azure OpenAI** – for Large Language Models (chat and embeddings).  
2. **Qdrant** – as a vector database for semantic document retrieval.  

These integrations ensure that generated quiz questions remain grounded in official certification content.

---

## Azure OpenAI Integration

- **Purpose:**  
  - Provides the **chat model (`gpt-4o`)** for template generation and question creation.  
  - Provides the **embedding model (`text-embedding-ada-002`)** for semantic indexing of certification documents.  

- **Connection:**  
  - Configured via `.env` file containing:  
    - `AZURE_OPENAI_API_KEY`  
    - `AZURE_OPENAI_ENDPOINT`  
    - `AZURE_OPENAI_API_VERSION`  
  - Access through the `langchain_openai` integration layer.  

- **Data flow:**  
  - Input: prompts and questions defined by the CrewAI Flow.  
  - Output: generated text (questions, templates, explanations).  

---

## Qdrant Integration

- **Purpose:**  
  - Stores vector embeddings of certification documents.  
  - Enables semantic similarity search to retrieve context-relevant passages for question generation.  

- **Deployment:**  
  - Runs as a Docker container locally on developer machines.  
  - Accessible via REST (`http://localhost:6333`) and gRPC (`http://localhost:6334`).  

- **Collection:**  
  - Current collection name: `qdrant_storage`.  
  - Stores embeddings generated from AI-900 documentation.  

- **Data flow:**  
  - Input: vector embeddings from `text-embedding-ada-002`.  
  - Output: semantically relevant chunks for RAG (used by `rag_crew`).  

---

## Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant CrewAI as QuizGenerator Flow
    participant Azure as Azure OpenAI
    participant Qdrant as Qdrant DB

    User->>CrewAI: Provides quiz configuration (provider, cert, topic, etc.)
    CrewAI->>Qdrant: Store/retrieve embeddings of certification docs
    CrewAI->>Azure: Request embeddings (text-embedding-ada-002)
    CrewAI->>Azure: Generate quiz questions (gpt-4o)
    Azure-->>CrewAI: Returns embeddings and generated content
    Qdrant-->>CrewAI: Returns relevant context chunks
    CrewAI-->>User: Outputs final quiz (JSON, Markdown, PDF)
