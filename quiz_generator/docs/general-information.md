# General Information

*(Template refs: EU AI Act Article 11; Annex IV ¶1–3)*

## Purpose and Intended Use

- **Purpose:**  
  To generate practice quizzes for IT certifications (e.g., Azure AI-900) based on official documentation.  
  The application guides the user through selecting **provider**, **certification**, **topic**, number and type of questions, and produces a complete quiz (template + generated questions + final output).

- **Intended Users:**  
  - Students and professionals preparing for certifications (e.g., Microsoft, AWS, etc.)  
  - Trainers or instructors who want to create support quizzes for courses  
  - Corporate L&D teams needing self-assessment tools  

- **Key Performance Indicators (KPIs):**  
  - Coverage of certification topics (alignment with official “skills measured”)  
  - Quality and clarity of generated questions (assessed via human review)  
  - User completion rate of quizzes  

- **Limitations and Prohibited Uses:**  
  - Does not replace studying official certification resources  
  - Generated questions may contain inaccuracies or ambiguities  
  - Must not be used during official exams or in violation of provider policies  

## Operational Environment

- **Expected operational environment:** Python 3.11+ on developer machines or a VM/container
- **Vector DB:** Qdrant (Docker) on `localhost:6333` / `6334`
- **LLM & Embeddings:** Azure OpenAI (configured via `.env`)
- **Datasets:** official certification PDFs stored in `src/quiz_generator/dataset/`

**Project setup (CLI-based with CrewAI):**

```bash
# 1) Create the virtual environment OUTSIDE the project folder
cd <your_workspace_root>
python -m venv .venv

# 2) Activate the venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3) Install CrewAI in the venv
pip install crewai

# 4) Obtain the project and move into the folder
# (if not already downloaded)
git clone https://github.com/simone-scaccia/FGBS_academy
cd FGBS_academy/quiz_generator

# 5) Start the Flow (CrewAI will resolve/install the Flow dependencies)
crewai flow kickoff


- **User Interface:**  
  - Command-line interface (interactive wizard via terminal)  
  - Outputs: JSON and Markdown files containing generated quizzes  

## Additional Information

- **Application Owners:** Simone Scaccia, Gabriele Tromboni, Beatrice Giacobbe, Flavia De Rinaldis  
- **Application Version:** v0.1  
- **Last Documentation Update:** 2025-09-09  
