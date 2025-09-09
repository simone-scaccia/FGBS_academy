# Cybersecurity

*(Template refs: Annex IV ¶2(j))*  

## Secret Management

- **API Keys:**  
  Azure OpenAI keys are stored in a local `.env` file.  
- **Best practices:**  
  - `.env` is excluded from version control via `.gitignore`.  
  - Keys are rotated periodically to reduce risk.  
- **Extensions:**  
  Secrets can be managed using Azure Key Vault or other enterprise-grade secret stores.  

---

## Data Protection

- **Dataset content:**  
  Certification PDFs are public documentation; no personal or sensitive data is processed.  
- **Logs:**  
  Logs do not contain user secrets or raw API keys.  
- **Isolation:**  
  All data (datasets, embeddings) remains local in the developer environment or controlled VM.  

---

## Network Security

- **Qdrant:**  
  Runs locally in Docker (`localhost:6333` and `6334`) with no external exposure.  
- **Outbound connections:**  
  Only outbound calls are made to Azure OpenAI endpoints.  
- **No public APIs exposed:**  
  The application has no externally accessible endpoints.  

---

## Access Control

- **User roles:**  
  Currently single-user CLI interaction; no multi-user or shared access.  
- **System access:**  
  Restricted to the developer’s machine or secured VM/container.  

---

## Threat Mitigation

- **Common risks addressed:**  
  - **Unauthorized access:** prevented by local isolation and secret management.  
  - **Data poisoning:** reduced by only allowing official certification PDFs.  
  - **Denial of service:** Flow fails gracefully when Qdrant or API limits are exceeded.  
- **Monitoring:**  
  Errors and failures are logged for audit and post-mortem analysis.  

---

## Compliance Considerations

- **GDPR / Data Privacy:** not applicable (no personal data processed).  
- **AI Act:** classified as *Limited risk* system; mitigations align with Annex IV guidance.  
