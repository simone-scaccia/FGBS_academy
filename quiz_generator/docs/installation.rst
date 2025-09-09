Installation
============

Requirements
------------

* Python 3.10–3.13 (see ``pyproject.toml``)
* ``crewai`` (installed via project deps)
* Qdrant running locally at ``http://localhost:6333`` (or a remote instance)
* Azure OpenAI access for embeddings (and optional chat LLM)

Installation Steps
------------------

1. Clone the repository
2. Create and activate a virtual environment (recommended)
3. Install dependencies using your preferred tool:

   .. code-block:: bash

      # using pip
      pip install -e .

      # or using uv (if installed)
      uv pip install -e .

4. Set up environment variables (see below)
5. Run the flow (see "Running" section)

Environment Variables
---------------------

Set these variables to use Azure OpenAI for embeddings (required) and, optionally, for the chat LLM:

.. code-block:: bash

   # Required for embeddings
   export AZURE_OPENAI_ENDPOINT="https://<your-endpoint>.openai.azure.com"
   export AZURE_OPENAI_API_KEY="<your-azure-openai-key>"
   export AZURE_OPENAI_API_VERSION="2024-02-01"   # default used if not set
   export EMB_MODEL_NAME="text-embedding-ada-002"

   # Optional for chat LLM inside RAG (only if you want LLM responses)
   export MODEL="gpt-4o-mini"                      # your Azure deployment/model name

Qdrant Configuration
--------------------

By default the app expects Qdrant at ``http://localhost:6333``. To use a remote instance, set:

.. code-block:: bash

   export QDRANT_URL="http://<host>:6333"

Running
-------

You can start the interactive flow (which asks you to select provider, certification, topic, number of questions, etc.) in two ways after installation:

.. code-block:: bash

   # Using console scripts defined in pyproject
   kickoff

   # Or via module entrypoint
   crewai flow kickoff

The flow will:
- initialize (or reuse) a Qdrant collection per provider/certification
- generate a quiz template
- create quiz questions using RAG
- write outputs under ``quiz_generator/outputs/`` (e.g., ``questions.json``, ``quiz.md``, ``quiz.pdf``)