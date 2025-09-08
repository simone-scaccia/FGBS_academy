from crewai.tools import tool
from typing import List
from langchain.document_loaders import PDFMinerLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from pathlib import Path
from qdrant_client import QdrantClient
from quiz_generator.tools.rag_qdrant_hybrid import Settings, retry_with_backoff
from quiz_generator.utils.qdrant_utils import get_embeddings, get_vector_size, recreate_collection_for_rag


def load_pdf(certification : str) -> List[Document]:
    """Correct path based on your project structure"""
    print(f"Loading PDFs for certification: {certification}")
    path = os.path.abspath(f"../dataset/azure/AI_900")
    documents: List[Document] = []

    for file in os.listdir(path):
        if file.endswith(".pdf"):
            file_path = os.path.join(path, file)
            loader = PDFMinerLoader(file_path, mode="page")
            docs = loader.load()
            for doc in docs:
                doc.metadata["topic"] = file
            documents.extend(docs)

    return documents



@tool("create_qdrant_DB")
def create_qdrant_DB(settings: Settings) -> QdrantClient:
    """Initilization of Qdrant client and collection creation"""

    client = QdrantClient(url=settings.qdrant_url, timeout=30)
    vector_size = retry_with_backoff(get_vector_size(get_embeddings(settings)), max_retries=5, base_delay=2.0)
    collection = recreate_collection_for_rag(client, settings, vector_size=vector_size)
    return collection

