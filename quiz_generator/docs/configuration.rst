Quiz Generator Configuration
===========================

This document describes the configuration for the `quiz_generator` project, which automates quiz creation using CrewAI and RAG (Retrieval-Augmented Generation) techniques.

Project Metadata
----------------
- **Name:** quiz_generator
- **Version:** 0.1.0
- **Description:** quiz_generator using CrewAI
- **Python Version:** >=3.10, <3.14
- **Main Dependencies:**
  - crewai[tools]
  - langchain, langchain-community, langchain-core, langchain-openai
  - openai
  - qdrant-client
  - markdown2, markdown-pdf, pdfkit, pymupdf
  - pytest
  - jsonpatch, jsonpointer

Entry Points
------------
- `kickoff`: Starts the quiz generation flow
- `run_crew`: Alias for kickoff
- `plot`: Generates a flow plot (see crewai_flow.html)

CrewAI Flow
-----------
The flow consists of the following steps:
1. Collect User Input
2. Initialize Vector Database
3. Generate Quiz Template
4. Generate Quiz With RAG Crew
5. Create Final Quiz
6. Finalize Flow

Configuration Example
--------------------
Configuration is typically provided via a JSON file (see `test_config.json`). Example:

.. code-block:: json

    {
      "test_config": {
        "provider": "azure",
        "certification": "AI_900",
        "topic": "First available topic",
        "number_of_questions": 7,
        "question_type": "mixed"
      },
      "expected_outputs": [
        "outputs/quiz_template.md",
        "outputs/questions.json",
        "outputs/quiz.md",
        "outputs/quiz.pdf",
        "outputs/completed_quiz.md",
        "outputs/quiz_evaluation.md"
      ],
      "expected_distribution": {
        "total": 7,
        "multiple_choice": 3,
        "true_false": 2,
        "open_ended": 2
      }
    }

