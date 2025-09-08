# Quiz Generator - CrewAI Flow Implementation

## Overview
This project has been refactored to follow CrewAI best practices by implementing a main Flow in `main.py` instead of using a separate database crew.

## Architecture Changes

### ✅ What was implemented:
1. **Main Flow in main.py**: Following CrewAI best practices, the main logic is now in `main.py`
2. **Direct database initialization**: Using `rag_qdrant_hybrid.py` directly for database setup
3. **RAG Crew integration**: The RAG crew now handles quiz generation with access to the RAG tool
4. **Removed database_crew**: Eliminated the separate database crew folder

### 🔄 Flow Process:
1. **User Selection**: Choose provider, certification, and topic
2. **Database Initialization**: Load and process PDFs from the selected certification using `rag_qdrant_hybrid.py`
3. **RAG Crew Execution**: Generate quiz using the configured RAG crew with access to the knowledge base

## Key Files Modified:

### `src/quiz_generator/main.py`
- Implements the main flow logic
- Handles user interaction for provider/certification/topic selection
- Integrates database initialization using `rag_qdrant_hybrid.py`
- Orchestrates the RAG crew execution

### `src/quiz_generator/crews/rag_crew/rag_crew.py`
- Added RAG tool to both researcher and reporting_analyst agents
- Updated to work with the main flow

### `src/quiz_generator/crews/rag_crew/config/agents.yaml`
- Updated agent roles for quiz generation focus
- Enhanced backstories for educational content creation

### `src/quiz_generator/crews/rag_crew/config/tasks.yaml`
- Modified tasks to focus on quiz generation
- Added comprehensive research and quiz creation workflows

### `src/quiz_generator/tools/rag_qdrant_hybrid.py`
- Updated to use Azure OpenAI embeddings correctly
- Fixed LLM initialization for Azure OpenAI
- Improved error handling and rate limiting

## Usage

```bash
# Navigate to the project directory
cd quiz_generator

# Run the quiz generator flow
python -m src.quiz_generator.main
```

## Flow Steps:
1. Select a provider (e.g., "azure")
2. Select a certification (e.g., "AI_900")  
3. Select a topic from available PDFs
4. Database automatically initializes with all PDFs from the certification
5. RAG crew generates comprehensive quiz questions
6. Results are saved to a timestamped file

## Environment Setup:
Ensure your `.env` file contains:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_ENDPOINT=your_endpoint_here
MODEL=gpt-4o
EMB_MODEL_NAME=text-embedding-ada-002
```

## Dependencies:
- CrewAI >=0.177.0
- LangChain Community for document loaders
- Qdrant client for vector database
- Azure OpenAI for embeddings and LLM

## Output:
The system generates comprehensive quiz files with:
- Multiple choice questions (4 options each)
- Detailed explanations for correct answers
- Difficulty levels (Beginner/Intermediate/Advanced)
- Source references from the knowledge base
- Timestamped filenames for organization
