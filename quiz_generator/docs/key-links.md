# Key Links

This page collects the essential links (Single Source of Truth) for the **Quiz Generator (CrewAI)** project.

## Repository & Project

- **Code repository:** [simone-scaccia/FGBS_academy](https://github.com/simone-scaccia/FGBS_academy)  
- **Main branch:** `main`  

## Documentation

- **Template structure:** see [Application Documentation Template](index.md)  
- **Architecture & Flow:** see [Application Functionality](application-functionality.md)  
- **Models & Datasets:** [Models](models.md) · [Datasets](datasets.md)

## Environments & Infrastructure

- **Local runtime (dev):** Python 3.11+ · `mkdocs serve`  
- **Local Vector DB (Qdrant):** `http://localhost:6333`  
  - **Qdrant Dashboard:** `http://localhost:6333/dashboard`  
- **Cloud account / Subscription:** Azure (certification documentation datasets)  
- **Document storage:** local dataset in `src/quiz_generator/dataset/`

## LLM & Secrets

- **LLM/Embeddings provider:** Azure OpenAI  
- **Chat model:** `gpt-4o`  
- **Embedding model:** `text-embedding-ada-002`  
- **Secrets management:** local `.env` file   

## Datasets / Sources

- **Root dataset (local):** `src/quiz_generator/dataset/`  
- **Supported certifications (initial):** `AI-900` (Azure AI Fundamentals)  
- **Official "skills measured" source:** [AI-900 Skills Measured - Microsoft Learn](https://learn.microsoft.com/en-us/credentials/certifications/exams/ai-900/)  
- **Other authorized sources:** official PDFs downloaded from Azure Docs  
- **Dataset update policy:** manual update when Microsoft releases new versions of the PDFs

## Observability & Operations

- **Troubleshooting index:** see [Incident Management](troubleshooting/deployment.md)

## Security & Compliance

- **Applied standards:** [Standards applied](standards-applied.md)  
- **EU Declaration of Conformity (if applicable):** [EU Declaration of conformity](eu-declaration-of-conformity.md)  

## Contacts

- **Product / App Owners:** Simone Scaccia, Gabriele Tromboni, Beatrice Giacobbe, Flavia De Rinaldis  
