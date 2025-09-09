Configuration
=============

This section describes how to configure the QA AI Agent system.

.. toctree::
   :maxdepth: 2

Configuration Options
---------------------

The system can be configured through various configuration files and environment variables.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

- ``OPENAI_API_KEY``: Your OpenAI API key for accessing GPT models
- ``SERPER_API_KEY``: API key for SerperDev web search functionality
- ``FAISS_INDEX_PATH``: Path to your FAISS index for RAG functionality

Configuration Files
~~~~~~~~~~~~~~~~~~~

The system uses YAML configuration files for agents and tasks:

- ``agents.yaml``: Defines the AI agents and their roles
- ``tasks.yaml``: Defines the tasks that agents can perform

Example Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # agents.yaml example
   agents:
     researcher:
       name: Research Agent
       role: Conducts research and gathers information
       goal: Find accurate and relevant information
     
     validator:
       name: Validation Agent
       role: Validates and verifies information
       goal: Ensure information accuracy and reliability
