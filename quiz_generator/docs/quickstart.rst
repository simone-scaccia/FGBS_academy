Quick Start
===========

Basic Usage
-----------

.. code-block:: python

   from .main import kickoff
   
   # Start the QA flow
   kickoff()

Example Flow
------------

1. User inputs a topic
2. System checks ethical considerations
3. Routes to appropriate crew (RAG or web search)
4. Retrieves and summarizes information
5. Outputs results to report.md

Configuration
-------------

Ensure your YAML configuration files are properly set up in the crew config directories.