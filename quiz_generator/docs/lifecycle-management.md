# Lifecycle Management

*(Template refs: Annex IV ¶2(h))*  

## Versioning

- **Source code:** managed with GitHub (`simone-scaccia/FGBS_academy`), main branch = `main`.  
- **Flow versioning:** each release of the Quiz Generator Flow is tagged in Git.  
- **Documentation:** versioned together with the source code; MkDocs site rebuilds per release.  

## Dataset Updates

- **Source:** official Microsoft Learn certification PDFs.  
- **Update policy:**  
  - Manually download new versions when Microsoft updates “skills measured” pages.  
  - Re-index updated documents into Qdrant by re-running the Flow initialization step.  
- **Traceability:** keep previous versions of PDFs in a separate archive folder if needed.  

## Dependency Management

- **CrewAI dependencies:** resolved automatically at `crewai flow kickoff`.  
- **External libraries:** updated periodically (LangChain, Qdrant client, dotenv, etc.).  
- **Strategy:** pin versions for stability in production, update regularly in development.  

## Monitoring & Quality

- **Question quality:** regularly reviewed by human experts.  
- **Coverage:** check that generated quizzes reflect the latest “skills measured”.  
- **Error handling:** Flow state logs errors (dataset missing, Qdrant not initialized, etc.).  

## Change Log

- **Minor changes:** bug fixes, dependency bumps, documentation updates.  
- **Major changes:** new certification support, new question types, architectural updates.  
- **Tracking:** changes are logged in Git commits and optionally a `CHANGELOG.md`.  

## Decommissioning

- If the project is deprecated, final documentation and last supported dataset version are archived.  
- Qdrant collections can be dropped and Docker volumes removed to free resources.  
