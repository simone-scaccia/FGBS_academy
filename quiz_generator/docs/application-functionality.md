# Application Functionality

*(Template refs: Article 11; Annex IV ¶1–3; Article 13)*

## Instructions for Use (Deployers)

- **Setup:**  
  - Create a Python virtual environment (`python -m venv .venv`) and activate it.  
  - Install dependencies including CrewAI (`pip install crewai`).  
  - Ensure Qdrant is running locally via Docker (`http://localhost:6333`).  
  - Provide LLM and Embedding configuration in a `.env` file.  

- **Run:**  
  - Start the flow:  
    ```bash
    crewai flow quiz_generator
    ```  
  - Follow the CLI wizard to select:  
    - Provider (e.g., Microsoft Azure)  
    - Certification (e.g., AI-900)  
    - Topic(s) of focus  
    - Number of questions  
    - Question type (True/False, Multiple Choice, Open-ended)  

- **Output:**  
  - A quiz template  
  - Generated questions enriched with context via RAG  
  - A final assembled quiz (JSON, Markdown, and PDF formats)

---

## Model Capabilities & Limitations

- **Capabilities:**  
  - Generates practice questions aligned with official certification documentation.  
  - Supports multiple question types (T/F, MCQ, Open-ended).  
  - Uses Retrieval-Augmented Generation (RAG) for improved factual grounding.  

- **Limitations:**  
  - Coverage is limited to the datasets indexed (official documentation PDFs).  
  - Possible inaccuracies or ambiguities in generated questions.  
  - No graphical user interface — interaction is CLI-only at present.  

---

## Input Data Requirements

- **Required datasets:**  
  - Certification documentation PDFs downloaded from Microsoft Learn (or equivalent vendor).  
- **Format:**  
  - Files stored in `src/quiz_generator/dataset/<provider>/<certification>/`  
  - Supported formats: `.pdf`, `.md`, `.txt` (as parsed by the document loaders).  

---

## Output Explanation

- **Template:**  
  - Generated section headers and question placeholders based on user choices.  

- **Generated questions:**  
  - JSON representation including question text, options, and correct answers.  

- **Final quiz:**  
  - Markdown, JSON, and PDF combining template + generated questions.  
  - Ready for human review and optional distribution.  

---

## System Architecture Overview

- **Components:**  
  1. **TemplateGeneratorCrew** → creates quiz structure.  
  2. **RagCrew** → retrieves relevant content from Qdrant and generates questions.  
  3. **QuizMakerCrew** → assembles final quiz output.  
  4. **Database Utils** → initializes and manages Qdrant collections.  
  5. **User Utils** → handles CLI inputs and summary display.  

- **Architecture Diagram (high-level):**

```mermaid
flowchart TD
    A[User Input via CLI] --> B[TemplateGeneratorCrew]
    B --> C[RagCrew (Qdrant + LLM)]
    C --> D[QuizMakerCrew]
    D --> E[Final Quiz Output: JSON/Markdown]
