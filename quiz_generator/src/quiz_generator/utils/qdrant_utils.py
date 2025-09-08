from __future__ import annotations
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Iterable, Tuple
 
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.document_loaders import PyPDFLoader, PDFMinerLoader
 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model
 
from qdrant_client.models import ScalarType
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    HnswConfigDiff,
    OptimizersConfigDiff,
    ScalarQuantization,
    ScalarQuantizationConfig,
    PayloadSchemaType,
    FieldCondition,
    MatchValue,
    MatchText,
    Filter,
    SearchParams,
    PointStruct,
)

CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIRECTORY_PATH = os.path.dirname(CURRENT_FILE_PATH)
 
# Load env vars
load_dotenv()
 
@dataclass
class Settings:
    """Config settings for RAG pipeline"""
    qdrant_url: str = "http://localhost:6333"  # Qdrant URL
    collection: str = "rag_chunks"             # Collection name
    emb_model_name: str = "embedding_model"  # Embedding model
    chunk_size: int = 1000                      # Chunk size
    chunk_overlap: int = 200                   # Overlap size
    top_n_semantic: int = 30                   # Candidates for semantic search
    top_n_text: int = 100                      # Candidates for text search
    final_k: int = 6                           # Final results count
    alpha: float = 0.75                        # Semantic weight
    text_boost: float = 0.20                   # Text boost
    use_mmr: bool = True                       # Use MMR diversification
    mmr_lambda: float = 0.6                    # MMR balance
    lm_base_env: str = "OPENAI_BASE_URL"       # LLM base URL env
    lm_key_env: str = "OPENAI_API_KEY"         # LLM API key env
    lm_model_env: str = "LMSTUDIO_MODEL"       # LLM model env
    use_cache: bool = True                     # Enable embedding cache
    cache_file: str = "embedding_cache.pkl"   # Cache file path
 
SETTINGS = Settings()

def recreate_collection_for_rag(client: QdrantClient, settings: Settings, vector_size: int):
    """Create Qdrant collection and indexes only if they don't exist"""
    if not client.collection_exists(settings.collection):
        client.create_collection(
            collection_name=settings.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            hnsw_config=HnswConfigDiff(m=32, ef_construct=256),
            optimizers_config=OptimizersConfigDiff(default_segment_number=2),
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(type=ScalarType.INT8, always_ram=False)
            ),
        )
        client.create_payload_index(settings.collection, "text", PayloadSchemaType.TEXT)
        for key in ["doc_id", "source", "title", "lang"]:
            client.create_payload_index(settings.collection, key, PayloadSchemaType.KEYWORD)
    # If collection exists, do nothing (reuse existing collection and indexes)
def get_embeddings(settings: Settings) -> AzureOpenAIEmbeddings:
    """Return Azure OpenAI embeddings"""
    return AzureOpenAIEmbeddings(model=settings.emb_model_name)

def get_vector_size(embeddings: AzureOpenAIEmbeddings) -> int:
    return len(embeddings.embed_query("hello world"))

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """Retry function with exponential backoff for rate limiting"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                if attempt == max_retries - 1:
                    raise e
                delay = base_delay * (2 ** attempt)
                print(f"Rate limit hit, waiting {delay} seconds before retry {attempt + 1}/{max_retries}")
                time.sleep(delay)
            else:
                raise e
    return None


def split_documents(docs: List[Document], settings: Settings) -> List[Document]:
    """Split docs into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", ", ", " ", ""],
    )
    return splitter.split_documents(docs)