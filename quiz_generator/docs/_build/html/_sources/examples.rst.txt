Quiz Generator Usage Examples
============================

This document provides usage examples for the `quiz_generator` project in the FGBS_academy repository.

Complete Flow Example
---------------------
The following Python script runs the complete quiz generation workflow with predefined inputs:

.. code-block:: python

    from src.quiz_generator.main import QuizGeneratorFlow
    quiz_flow = QuizGeneratorFlow()
    quiz_flow.kickoff()

This will:
- Collect user input (provider, certification, topic, number of questions, question type)
- Initialize the vector database
- Generate a quiz template
- Generate questions using RAG Crew
- Create the final quiz
- Finalize the flow

Automated Test Example
----------------------
Automated tests are provided in `test_complete_flow.py` and `test_azure_ai900.py`. Example:

.. code-block:: python

    # test_azure_ai900.py
    def test_azure_ai900_mixed_7_questions():
        quiz_flow = QuizGeneratorFlow()
        quiz_flow.state.provider = 'azure'
        quiz_flow.state.certification = 'AI_900'
        quiz_flow.state.topic = 'First available topic'
        quiz_flow.state.number_of_questions = 7
        quiz_flow.state.question_type = 'mixed'
        quiz_flow.initialize_vector_database()
        quiz_flow.generate_quiz_template()
        quiz_flow.generate_quiz_with_rag_crew()
        quiz_flow.create_final_quiz()
        quiz_flow.take_quiz()
        quiz_flow.evaluate_quiz()
        quiz_flow.finalize_flow()

Output Files
------------
After running the flow, the following files are generated in the `outputs/` directory:
- quiz_template.md
- questions.json
- quiz.md
- quiz.pdf
- completed_quiz.md
- quiz_evaluation.md

Flow Visualization
------------------
A flow plot is generated as `crewai_flow.html` to visualize the steps and connections in the quiz generation process.
