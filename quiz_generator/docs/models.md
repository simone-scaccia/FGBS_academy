# Models

*(Template refs: Annex IV ¶2(d))*  

## Overview

The Quiz Generator (CrewAI) application relies on Azure OpenAI models for both **question generation** and **document embedding**.

## Chat Model

- **Model name:** `gpt-4o`  
- **Provider:** Azure OpenAI  
- **Use case:**  
  - Generates the quiz template structure.  
  - Creates questions (True/False, MCQ, Open-ended) enriched with context retrieved from Qdrant.  
- **Strengths:**  
  - Supports multi-turn reasoning and context-aware question generation.  
  - Handles natural language prompts effectively.  
- **Limitations:**  
  - May generate ambiguous or overly complex questions if the input dataset lacks clarity.  
  - Requires human review before distribution.  

## Embedding Model

- **Model name:** `text-embedding-ada-002`  
- **Provider:** Azure OpenAI  
- **Use case:**  
  - Encodes certification documentation into vector representations.  
  - Enables semantic search and retrieval within Qdrant.  
- **Strengths:**  
  - Lightweight, cost-effective embeddings.  
  - Optimized for semantic similarity search.  
- **Limitations:**  
  - Cannot capture full reasoning or multi-step logic (embedding only encodes meaning).  
  - Performance depends on the quality and coverage of the source documents.  

## Model Integration

- Embeddings are generated at dataset initialization and stored in Qdrant.  
- The chat model (`gpt-4o`) is invoked during quiz template generation and question creation.  
- Both models are orchestrated through CrewAI Flows to ensure a modular and scalable pipeline.
