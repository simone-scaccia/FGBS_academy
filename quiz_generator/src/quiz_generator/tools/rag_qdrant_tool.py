"""CrewAI tool that wraps simple RAG retrieval utilities.

Accepts a question and a ``k`` value to retrieve top-k contexts from a local
vector store. Useful as an agent tool step before generation.
"""

from typing import Type, List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .rag_qdrant_hybrid import search_rag, search_rag_with_collection


class RagToolInput(BaseModel):
    """Input schema for ``RagTool``."""
    question: str = Field(..., description="Question to answer using RAG search.")
    k: int = Field(3, description="Number of documents to retrieve for context.")


class RagTool(BaseTool):
    """CrewAI tool that performs a simple RAG retrieval with support for specific collections."""

    name: str = "RAG Search Tool"
    description: str = (
        "A tool that performs a Retrieval-Augmented Generation (RAG) search "
        "given a question and a number of documents to retrieve. "
        "Uses a local vector store and LLM to retrieve and answer based on "
        "context. Returns a list of document strings with source and content information."
    )
    args_schema: Type[BaseModel] = RagToolInput
    
    # Class attributes for provider/certification configuration
    provider: Optional[str] = None
    certification: Optional[str] = None
    
    def __init__(self, provider: Optional[str] = None, certification: Optional[str] = None, **kwargs):
        """
        Initialize RagTool with optional provider/certification for collection selection.
        
        Args:
            provider (str, optional): Provider name for collection selection
            certification (str, optional): Certification name for collection selection
        """
        super().__init__(**kwargs)
        self.provider = provider
        self.certification = certification

    def _run(self, question: str, k: int) -> List[str]:
        """Run retrieval with the provided inputs."""
        if not question:
            raise ValueError("Please provide a question for RAG search.")
        
        # Use collection-specific search if provider/certification are set
        if self.provider and self.certification:
            results = search_rag_with_collection(
                question, 
                k=k, 
                provider=self.provider, 
                certification=self.certification
            )
        else:
            # Fallback to default search
            results = search_rag(question, k=k)

        return results
