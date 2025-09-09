# Risk Mitigation Measures

*(Template refs: Annex IV ¶2(i))*  

## Preventive Measures

- **Grounding with official documentation:**  
  All quiz questions are generated using Retrieval-Augmented Generation (RAG) with embeddings from official certification PDFs. This reduces the risk of hallucinated or irrelevant content.  

- **Topic filtering:**  
  The Flow enforces topic selection aligned with the “skills measured” of the chosen certification.  

- **Input validation:**  
  User inputs (provider, certification, number of questions, type) are validated before execution to prevent invalid configurations.  

---

## Protective Measures

- **Human review:**  
  Generated quizzes are intended for human review before distribution to students or trainees.  

- **Error logging:**  
  Flow state logs capture errors (e.g., dataset missing, Qdrant not initialized). Errors prevent progression to the next step, avoiding corrupted outputs.  

- **Fallbacks:**  
  If Qdrant retrieval fails, the Flow aborts gracefully with an error message instead of producing low-quality results.  

---

## Security Measures

- **Secret management:**  
  Azure OpenAI API keys are stored in a local `.env` file (optionally integrable with Azure Key Vault).  

- **Local isolation:**  
  Qdrant runs in a local Docker container, minimizing exposure to external access.  

- **Access control:**  
  No external API is exposed by default; only local CLI interaction is possible.  

---

## Corrective Measures

- **Dataset reinitialization:**  
  If errors occur due to corrupted embeddings or collection mismatch, the Qdrant collection can be dropped and re-created.  

- **Rollback procedures:**  
  Code and dataset versions are tracked with Git; rollback to a previous stable state is always possible.  

- **Continuous improvement:**  
  Feedback from users and trainers is incorporated into future versions of the Flow to reduce recurring issues.  
