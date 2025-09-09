# Troubleshooting AI Application Deployment

*(Template refs: Annex IV ¶2(l))*  

## Common Deployment Issues

### 1. Virtual environment not activated
- **Symptom:** `command not found: crewai`  
- **Cause:** the `.venv` was created but not activated before running commands.  
- **Mitigation:**  
  ```bash
  # Windows
  .\.venv\Scripts\activate
  # Linux/macOS
  source .venv/bin/activate

### 2. Missing dependencies
- **Symptom:** `ModuleNotFoundError: No module named 'langchain_openai'`  
- **Cause:** dependencies not installed correctly.  
- **Mitigation:** run the Flow setup inside the project:  
  ```bash
  crewai flow kickoff

### 3. Qdrant container not running
- **Symptom:** `ConnectionError: Failed to connect to localhost:6333`  
- **Cause:** Qdrant Docker container not started.  
- **Mitigation:**  
  ```bash
  docker start qdrant
  # or if not created yet:
  docker run --name qdrant \
    -p 6333:6333 -p 6334:6334 \
    -v qdrant-storage:/qdrant/storage \
    qdrant/qdrant:latest

### 4. Invalid `.env` configuration
- **Symptom:** `AuthenticationError: invalid API key`  
- **Cause:** Azure OpenAI API key or endpoint not set correctly.  
- **Mitigation:** check that `.env` contains valid values, for example:
```  
AZURE_OPENAI_API_KEY=xxxx
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
```
### 5. Missing dataset
- **Symptom:** `Error during database initialization`  
- **Cause:** certification PDFs are missing in `src/quiz_generator/dataset/`.  
- **Mitigation:** download the official documentation PDFs from Microsoft Learn and place them in the dataset folder.  

