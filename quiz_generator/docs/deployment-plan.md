# Deployment Plan

*(Template refs: Annex IV ¶2(g))*  

## Deployment Environments

- **Development:**  
  - Local machine with Python 3.11+  
  - Qdrant running in Docker on `localhost:6333`  
  - `.env` file for Azure OpenAI credentials  
  - Documentation browsed via MkDocs (`mkdocs serve`)  

- **Staging (optional):**  
  - Virtual machine or containerized environment replicating production setup  
  - Used for integration testing and QA before release  

- **Production (optional):**  
  - Could be deployed in a cloud VM or containerized service (Docker/Kubernetes)  
  - Centralized Qdrant instance (managed or hosted)  
  - Secure secret management (e.g., Azure Key Vault instead of local `.env`)  

---

## Deployment Steps


1. **Set up environment (outside the project)**
   ```bash
   # Create and activate a virtual environment
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   # source .venv/bin/activate

   # Install CrewAI in the venv
   pip install crewai

   # Move into the project directory
    cd quiz_generator

    # Launch the Flow (CrewAI will handle dependencies automatically)
    crewai flow kickoff



