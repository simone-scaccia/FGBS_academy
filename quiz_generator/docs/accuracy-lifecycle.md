# Accuracy Throughout the Lifecycle

*(Template refs: Annex IV ¶2(j))*  

## Data Accuracy

- **Source quality:**  
  All questions are grounded in official Microsoft Learn documentation (AI-900 initially).  
  Using authoritative PDFs minimizes the risk of inaccurate or outdated content.  

- **Preprocessing checks:**  
  Documents are validated before ingestion (format checks, duplicates removed).  
  Qdrant indexing ensures consistent embedding storage.  

---

## Model Accuracy

- **Embeddings:**  
  `text-embedding-ada-002` provides semantic similarity for document retrieval.  
  Accuracy of retrieval is validated by checking that retrieved chunks align with the selected topic.  

- **Question generation:**  
  `gpt-4o` is used for natural language question creation.  
  Human reviewers validate clarity, correctness, and relevance of generated questions.  

---

## Lifecycle Validation

- **Initial validation:**  
  Each new certification dataset is tested by generating a small quiz (smoke test).  
  Outputs are checked manually for accuracy and coverage.  

- **Ongoing validation:**  
  Regular re-checks whenever documentation is updated or dependencies are upgraded.  

- **Regression testing:**  
  If quiz generation degrades after an update, previous Flow versions and datasets can be rolled back.  

---

## User Feedback Loop

- **Trainer review:**  
  Trainers and subject-matter experts review quiz quality and flag incorrect or misleading questions.  

- **Continuous improvement:**  
  Feedback is incorporated into dataset updates and Flow refinements.  
  This ensures that accuracy is maintained throughout the lifecycle of the application.  
