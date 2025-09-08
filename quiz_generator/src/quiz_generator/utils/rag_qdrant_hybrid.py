"""
RAG pipeline with Qdrant and AzureOpenAI embeddings
"""
 
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

from langchain_community.document_loaders import PyPDFLoader, PDFMinerLoader
 
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
    collection: str = "rag_chunks"             # Collection name (can be dynamic)
    emb_model_name: str = "text-embedding-ada-002"  # Embedding model
    chunk_size: int = 10000                      # Chunk size
    chunk_overlap: int = 300                   # Overlap size
    top_n_semantic: int = 30                   # Candidates for semantic search
    top_n_text: int = 100                      # Candidates for text search
    final_k: int = 6                           # Final results count
    alpha: float = 0.75                        # Semantic weight
    text_boost: float = 0.20                   # Text boost
    use_mmr: bool = True                       # Use MMR diversification
    mmr_lambda: float = 0.6                    # MMR balance
    lm_base_env: str = "AZURE_OPENAI_ENDPOINT" # LLM base URL env
    lm_key_env: str = "AZURE_OPENAI_API_KEY"   # LLM API key env
    lm_model_env: str = "MODEL"                # LLM model env
    use_cache: bool = True                     # Enable embedding cache
    cache_file: str = "embedding_cache.pkl"   # Cache file path

def get_collection_name(provider: str, certification: str) -> str:
    """
    Generate a unique collection name for each provider/certification combination.
    
    Args:
        provider (str): The provider name (e.g., 'azure')
        certification (str): The certification name (e.g., 'AI_900')
        
    Returns:
        str: Collection name in format: provider_certification_chunks
    """
    # Clean the names to ensure valid collection names (alphanumeric + underscore)
    clean_provider = "".join(c if c.isalnum() else "_" for c in provider.lower())
    clean_certification = "".join(c if c.isalnum() else "_" for c in certification.lower())
    
    return f"{clean_provider}_{clean_certification}_chunks"


def get_settings_for_certification(provider: str, certification: str) -> Settings:
    """
    Get Settings instance with collection name specific to provider/certification.
    
    Args:
        provider (str): The provider name
        certification (str): The certification name
        
    Returns:
        Settings: Settings instance with specific collection name
    """
    settings = Settings()
    settings.collection = get_collection_name(provider, certification)
    return settings
 
SETTINGS = Settings()
 
# ========== Embeddings & LLM ==========

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

def get_embeddings(settings: Settings) -> AzureOpenAIEmbeddings:
    """Return Azure OpenAI embeddings"""
    return AzureOpenAIEmbeddings(
        model=settings.emb_model_name,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    )
 
def get_llm(settings: Settings):
    """Initialize LLM if configured"""
    try:
        endpoint = os.getenv(settings.lm_base_env)
        key = os.getenv(settings.lm_key_env)
        model_name = os.getenv(settings.lm_model_env)
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        
        if not (endpoint and key and model_name):
            print("LLM not configured - missing environment variables")
            return None
            
        llm = init_chat_model(
            model_name, 
            model_provider="azure_openai",
            azure_endpoint=endpoint,
            api_key=key,
            api_version=api_version
        )
        
        # Test the LLM
        test_response = llm.invoke("test")
        if test_response:
            print("LLM configured successfully")
            return llm
        print("LLM test failed")
        return None
    except Exception as e:
        print(f"LLM error: {e}")
        return None
 
# ========== Data prep ==========

def load_pdf(file_path : str) -> List[Document]:
    """Load PDF with suppressed warnings for problematic PDF formatting."""
    import warnings
    import logging
    
    # Suppress specific PDF parsing warnings
    warnings.filterwarnings("ignore", message=".*Cannot set gray.*")
    warnings.filterwarnings("ignore", message=".*Cannot get FontBBox.*")
    
    # Temporarily disable pdfminer logs
    pdfminer_logger = logging.getLogger('pdfminer')
    original_level = pdfminer_logger.level
    pdfminer_logger.setLevel(logging.ERROR)
    
    documents: List[Document] = []
    
    try:
        loader = PDFMinerLoader(file_path)
        docs = loader.load()
        
        for doc in docs:
                doc.metadata["source"] = os.path.basename(file_path)
                documents.append(doc)
    finally:
        # Restore original logging level
        pdfminer_logger.setLevel(original_level)

    return documents

def split_documents(docs: List[Document], settings: Settings) -> List[Document]:
    """Split docs into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", ", ", " ", ""],
    )
    return splitter.split_documents(docs)
 
# ========== Qdrant ==========
 
def get_qdrant_client(settings: Settings) -> QdrantClient:
    """Return Qdrant client"""
    return QdrantClient(url=settings.qdrant_url, timeout=30)



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

# ========== Ingest ==========
 
def build_points(chunks: List[Document], embeds: List[List[float]]) -> List[PointStruct]:
    """Build Qdrant points"""
    pts: List[PointStruct] = []
    for i, (doc, vec) in enumerate(zip(chunks, embeds), start=1):
        payload = {
            "doc_id": doc.metadata.get("id"),
            "source": doc.metadata.get("source"),
            "title": doc.metadata.get("title"),
            "lang": doc.metadata.get("lang", "en"),
            "text": doc.page_content,
            "chunk_id": i - 1
        }
        pts.append(PointStruct(id=i, vector=vec, payload=payload))
    return pts
 
def upsert_chunks(client: QdrantClient, settings: Settings, chunks: List[Document], embeddings: AzureOpenAIEmbeddings):
    """Embed and upsert chunks with rate limiting"""
    print(f"Embedding {len(chunks)} chunks...")
    
    # Process chunks in smaller batches to avoid rate limits
    batch_size = 10  # Reduce batch size for rate limiting
    all_vecs = []
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
        
        # Use retry logic for embedding
        def embed_batch():
            return embeddings.embed_documents([c.page_content for c in batch])
        
        batch_vecs = retry_with_backoff(embed_batch, max_retries=5, base_delay=2.0)
        all_vecs.extend(batch_vecs)
        
        # Add small delay between batches
        if i + batch_size < len(chunks):
            time.sleep(1.0)
    
    points = build_points(chunks, all_vecs)
    client.upsert(collection_name=settings.collection, points=points, wait=True)
 
# ========== Search ==========
 
def qdrant_semantic_search(client: QdrantClient, settings: Settings, query: str, embeddings: AzureOpenAIEmbeddings, limit: int, with_vectors: bool = False):
    """Semantic search in Qdrant with retry logic"""
    def embed_query():
        return embeddings.embed_query(query)
    
    qv = retry_with_backoff(embed_query, max_retries=5, base_delay=2.0)
    res = client.query_points(
        collection_name=settings.collection,
        query=qv,
        limit=limit,
        with_payload=True,
        with_vectors=with_vectors,
        search_params=SearchParams(hnsw_ef=256, exact=False),
    )
    return res.points
 
def qdrant_text_prefilter_ids(client: QdrantClient, settings: Settings, query: str, max_hits: int) -> List[int]:
    """Return ids matching text filter"""
    matched_ids: List[int] = []
    next_page = None
    while True:
        points, next_page = client.scroll(
            collection_name=settings.collection,
            scroll_filter=Filter(must=[FieldCondition(key="text", match=MatchText(text=query))]),
            limit=min(256, max_hits - len(matched_ids)),
            offset=next_page,
            with_payload=False,
            with_vectors=False,
        )
        matched_ids.extend([p.id for p in points])
        if not next_page or len(matched_ids) >= max_hits:
            break
    return matched_ids
 
def mmr_select(query_vec: List[float], candidates_vecs: List[List[float]], k: int, lambda_mult: float) -> List[int]:
    """Select diverse results with MMR"""
    import numpy as np
    V = np.array(candidates_vecs, dtype=float)
    q = np.array(query_vec, dtype=float)
    def cos(a, b):
        na = (a @ a) ** 0.5 + 1e-12
        nb = (b @ b) ** 0.5 + 1e-12
        return float((a @ b) / (na * nb))
    sims = [cos(v, q) for v in V]
    selected: List[int] = []
    remaining = set(range(len(V)))
    while len(selected) < min(k, len(V)):
        if not selected:
            best = max(remaining, key=lambda i: sims[i])
            selected.append(best)
            remaining.remove(best)
            continue
        best_idx = None
        best_score = -1e9
        for i in remaining:
            max_div = max([cos(V[i], V[j]) for j in selected]) if selected else 0.0
            score = lambda_mult * sims[i] - (1 - lambda_mult) * max_div
            if score > best_score:
                best_score = score
                best_idx = i
        selected.append(best_idx)
        remaining.remove(best_idx)
    return selected
 
def hybrid_search(client: QdrantClient, settings: Settings, query: str, embeddings: AzureOpenAIEmbeddings):
    """Hybrid search with semantic + text + MMR"""
    sem = qdrant_semantic_search(client, settings, query, embeddings, limit=settings.top_n_semantic, with_vectors=True)
    if not sem: return []
    text_ids = set(qdrant_text_prefilter_ids(client, settings, query, settings.top_n_text))
    scores = [p.score for p in sem]
    smin, smax = min(scores), max(scores)
    def norm(x): return 1.0 if smax == smin else (x - smin) / (smax - smin)
    fused: List[Tuple[int, float, Any]] = []
    for idx, p in enumerate(sem):
        base = norm(p.score)
        fuse = settings.alpha * base
        if p.id in text_ids:
            fuse += settings.text_boost
        fused.append((idx, fuse, p))
    fused.sort(key=lambda t: t[1], reverse=True)
    if settings.use_mmr:
        def embed_mmr_query():
            return embeddings.embed_query(query)
        
        qv = retry_with_backoff(embed_mmr_query, max_retries=5, base_delay=2.0)
        N = min(len(fused), max(settings.final_k * 5, settings.final_k))
        cut = fused[:N]
        vecs = [sem[i].vector for i, _, _ in cut]
        mmr_idx = mmr_select(qv, vecs, settings.final_k, settings.mmr_lambda)
        return [cut[i][2] for i in mmr_idx]
    return [p for _, _, p in fused[:settings.final_k]]
 
# ========== Prompt/Chain ==========
 
def format_docs_for_prompt(points: Iterable[Any]) -> str:
    """Format docs with sources"""
    blocks = []
    for p in points:
        pay = p.payload or {}
        src = pay.get("source", "unknown")
        blocks.append(f"[source:{src}] {pay.get('text','')}")
    return "\n\n".join(blocks)
 
def build_rag_chain(llm):
    """Build RAG chain with citations"""
    system_prompt = (
        "Sei un assistente tecnico. Rispondi in italiano. Usa solo CONTENUTO. "
        "Se non c'è, dichiara che non è presente. Cita sempre le fonti."
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Domanda:\n{question}\n\nCONTENUTO:\n{context}\n\nIstruzioni:\n1) Rispondi solo col contenuto.\n2) Cita fonti.\n3) Niente invenzioni.")
    ])
    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
 
# ========== Main ==========
 
def search_rag_with_collection(q, k, provider=None, certification=None):
    """
    RAG search with support for specific provider/certification collections.
    
    Args:
        q (str): Query string
        k (int): Number of results to return
        provider (str, optional): Provider name for collection selection
        certification (str, optional): Certification name for collection selection
        
    Returns:
        List of documents from hybrid search
    """
    print(f"--------- Starting RAG Search (Collection: {provider}_{certification}) -----------")
    
    # Get settings for specific certification if provided
    if provider and certification:
        s = get_settings_for_certification(provider, certification)
        print(f"🗄️ Using collection: {s.collection}")
    else:
        s = Settings()
        print(f"🗄️ Using default collection: {s.collection}")
    
    s.final_k = k
    embeddings = get_embeddings(s)
    client = get_qdrant_client(s)
    
    # Check if collection exists
    if not client.collection_exists(s.collection):
        print(f"❌ Collection '{s.collection}' not found. Please initialize the database first.")
        return []
    
    # Perform hybrid search
    hits = hybrid_search(client, s, q, embeddings)
    
    results = []
    for hit in hits:
        source = hit.payload.get("source", "Unknown")
        content = hit.payload.get("text", "")
        results.append(f"Source: {source}\nContent: {content}")
    
    return results


# Legacy function for backward compatibility
def search_rag(q, k):
    """Demo full RAG pipeline (legacy version)"""
    print("--------- Starting RAG Search -----------")
    s = SETTINGS
    s.final_k = k
    embeddings = get_embeddings(s)
    llm = get_llm(s)
    client = get_qdrant_client(s)
    # docs = simulate_corpus()
    docs = load_pdf(f"{CURRENT_DIRECTORY_PATH}/knowledge_base/EU AI Act.pdf")
    chunks = split_documents(docs, s)
    print(f"Docs: {len(docs)}, Chunks: {len(chunks)}")
    
    # Use retry logic for initial embedding call
    def get_vector_size():
        return len(embeddings.embed_query("hello world"))
    
    vector_size = retry_with_backoff(get_vector_size, max_retries=5, base_delay=2.0)
    recreate_collection_for_rag(client, s, vector_size)
    
    # You only need to run upsert_chunks if your collection is empty or you want to update it.
    # If the chunks are already embedded and present in Qdrant, you can skip this step.
    if not client.count(collection_name=s.collection).count:
        upsert_chunks(client, s, chunks, embeddings)
    else:
        print("Collection already populated, skipping upsert.")
    
    
    hits = hybrid_search(client, s, q, embeddings)
    if not hits:
        print("No result.")
        
    return format_docs_for_prompt(hits)

if __name__ == "__main__":
    print(search_rag("Quali sono i principi dell'AI etica?", 30))
    

