# Human Oversight

*(Template refs: Annex IV ¶2(k))*  

## Role of Human Oversight

- The Quiz Generator (CrewAI) is a **support tool** for learning and exam preparation.  
- **Humans remain in control** of all outcomes: generated quizzes are not final until reviewed.  
- The system provides drafts of quizzes, but distribution to students or trainees requires human approval.  

---

## Review Process

- **Trainer/Reviewer tasks:**  
  - Validate accuracy of generated questions.  
  - Check clarity and remove ambiguities.  
  - Ensure alignment with official certification “skills measured”.  
- **Feedback loop:**  
  - Review comments are incorporated into dataset updates and Flow refinements.  

---

## Safety Measures

- **Fail-safe defaults:**  
  If errors occur (e.g., missing dataset, failed retrieval), the Flow aborts instead of producing potentially misleading quizzes.  
- **Transparency:**  
  Each quiz includes metadata about its source (provider, certification, topic, number of questions).  
- **Traceability:**  
  Errors and warnings are logged, allowing reviewers to understand why a quiz may not be complete.  

---

## Accountability

- **Final responsibility:**  
  Human reviewers are accountable for approving or rejecting generated quizzes.  
- **Non-automated use:**  
  The tool cannot autonomously distribute content or replace official study material.  
- **Governance alignment:**  
  Oversight practices align with EU AI Act requirements for *Limited-risk* AI systems.  
