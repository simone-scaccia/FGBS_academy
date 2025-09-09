Installation
============

Requirements
------------

* Python 3.8+
* CrewAI
* LangChain
* FAISS
* Azure OpenAI API access

Installation Steps
------------------

1. Clone the repository
2. Install dependencies: ``pip install -r requirements.txt``
3. Set up environment variables
4. Configure YAML files

Environment Variables
---------------------

Set these environment variables for Azure OpenAI access:

.. code-block:: bash

   export AZURE_API_KEY="your-api-key"
   export AZURE_API_BASE="your-endpoint"
   export AZURE_API_VERSION="2024-02-15-preview"
   export EMBEDDING_MODEL="text-embedding-ada-002"