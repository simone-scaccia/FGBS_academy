Examples
========

This section provides practical examples of how to use the QA AI Agent system.

.. toctree::
   :maxdepth: 2

Basic Usage Examples
--------------------

Simple Question Answering
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qa_ai_agent.main import QA_AI_Agent
   
   # Initialize the agent
   agent = QA_AI_Agent()
   
   # Ask a simple question
   response = agent.ask("What is artificial intelligence?")
   print(response)

RAG-based Question Answering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qa_ai_agent.crews.rag_crew import RagCrew
   
   # Initialize RAG crew
   rag_crew = RagCrew()
   
   # Ask a question that requires document retrieval
   response = rag_crew.process_question(
       "What are the main features of our product?",
       context_docs=["product_manual.pdf", "specifications.txt"]
   )
   print(response)

Web Search Integration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qa_ai_agent.crews.web_search_crew import WebSearchCrew
   
   # Initialize web search crew
   web_crew = WebSearchCrew()
   
   # Search for current information
   response = web_crew.search_and_answer(
       "What are the latest developments in AI?",
       max_results=5
   )
   print(response)

Advanced Examples
-----------------

Custom Tool Integration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qa_ai_agent.tools.custom_tool import RagTool
   
   # Create a custom RAG tool
   rag_tool = RagTool(
       name="Document Q&A",
       description="Answer questions based on document content"
   )
   
   # Use the tool
   result = rag_tool.run("What is the main topic?", documents=["doc1.txt"])
   print(result)

Multi-Agent Workflow
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qa_ai_agent.crews.ethic_checker_crew import EthicCheckerCrew
   
   # Initialize ethic checker crew
   ethic_crew = EthicCheckerCrew()
   
   # Check content for ethical concerns
   ethic_report = ethic_crew.check_content(
       "Analyze this content for potential bias",
       content="Your content here..."
   )
   print(ethic_report)
