# Robustness

*(Template refs: Annex IV ¶2(j))*  

## Input Robustness

- **Validation of user input:**  
  - Provider, certification, topic, number of questions, and question type are validated before quiz generation.  
  - Invalid configurations prevent the Flow from progressing to avoid producing corrupted outputs.  

- **Edge cases:**   
  - Flow degrades gracefully with warnings instead of failing silently.  

---

## System Robustness

- **Failure isolation:**  
  Each Flow step (user input, database initialization, template generation, RAG question creation, final assembly) is isolated.  
  If one step fails, the process stops and logs the error, preventing propagation of corrupted data.  

- **Qdrant reliability:**  
  If the Qdrant collection is missing or corrupted, the Flow detects the issue and suggests reinitialization.  
  Errors such as “collection mismatch” or “empty request” are handled gracefully.  

---

## Model Robustness

- **Embeddings:**  
  Semantic search is resilient to slight variations in query phrasing.  
  Retrieval ensures coverage even if the topic wording differs from the documentation.  

- **Question generation:**  
  The model (`gpt-4o`) is prompted with structured templates to reduce variance and hallucination.  
  If context is missing, the system falls back to producing fewer questions rather than inaccurate ones.  

---

## Operational Robustness

- **Logging:**  
  Detailed logs are kept for each Flow step to allow troubleshooting and reproduction of issues.  

- **Rollback:**  
  If a failure occurs, code and datasets can be rolled back to previous stable versions.  

- **Recovery:**  
  Dropping and recreating the Qdrant collection allows recovery from index corruption.  

---

## Continuous Testing

- **Smoke tests:** small quiz generations are run after updates to validate end-to-end functioning.  
- **Stress tests:** attempted with large input datasets to ensure the Flow remains stable.  
- **User feedback:** incorporated continuously to refine robustness over time.  
