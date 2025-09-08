"""
Database utilities for Quiz Generator application.
This module contains functions for database initialization and management.
"""

import os
from datetime import datetime
from .rag_qdrant_hybrid import (
    get_embeddings, 
    get_qdrant_client, 
    recreate_collection_for_rag, 
    split_documents, 
    upsert_chunks,
    load_pdf,
    get_settings_for_certification,
    get_collection_name,
    retry_with_backoff
)


def initialize_database(provider, certification, dataset_base_path):
    """
    Initialize Qdrant database with documents from the specified provider and certification.
    Each provider/certification gets its own collection for better organization.
    
    Args:
        provider (str): The provider name
        certification (str): The certification name
        dataset_base_path (str): Base path to the dataset folder
        
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    print(f"🚀 Initializing Qdrant database...")
    print(f"📋 Provider: {provider}")
    print(f"🎓 Certification: {certification}")
    
    try:
        # Get settings specific to this certification
        settings = get_settings_for_certification(provider, certification)
        collection_name = get_collection_name(provider, certification)
        
        print(f"🗄️ Collection name: {collection_name}")
        
        embeddings = get_embeddings(settings)
        client = get_qdrant_client(settings)
        
        # Check if collection already exists and has data
        if client.collection_exists(settings.collection):
            collection_count = client.count(collection_name=settings.collection).count
            if collection_count > 0:
                print(f"✅ Collection '{collection_name}' already exists with {collection_count} documents")
                print("⏭️ Skipping database initialization (reusing existing collection)")
                return True
        
        # Load all PDF documents from the certification folder
        dataset_path = os.path.join(dataset_base_path, provider, certification)
        pdf_files = [f for f in os.listdir(dataset_path) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"❌ No PDF files found in {dataset_path}")
            return False
        
        print(f"📚 Found {len(pdf_files)} PDF files to process")
        
        all_documents = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(dataset_path, pdf_file)
            print(f"📄 Loading {pdf_file}...")
            documents = load_pdf(pdf_path)
            all_documents.extend(documents)
        
        print(f"📄 Loaded {len(all_documents)} documents")
        
        # Split documents into chunks
        chunks = split_documents(all_documents, settings)
        print(f"🔪 Split into {len(chunks)} chunks")
        
        # Get vector size for collection creation
        def get_vector_size():
            return len(embeddings.embed_query("hello world"))
        
        vector_size = retry_with_backoff(get_vector_size, max_retries=5, base_delay=2.0)
        
        # Create or recreate collection
        recreate_collection_for_rag(client, settings, vector_size)
        
        # Upsert chunks to database
        print("📥 Upserting chunks to database...")
        upsert_chunks(client, settings, chunks, embeddings)
        
        print("✅ Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        return False


def save_quiz_results(provider, certification, topic, crew_result, output_dir):
    """
    Save quiz generation results to a file.
    
    Args:
        provider (str): Selected provider
        certification (str): Selected certification
        topic (str): Selected topic
        crew_result: Result from the crew execution
        output_dir (str): Directory to save the output file
        
    Returns:
        str: Filename of the saved file
    """
    output_filename = f"quiz_{provider}_{certification}_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Quiz Generator Results\n")
        f.write(f"=" * 50 + "\n")
        f.write(f"Provider: {provider}\n")
        f.write(f"Certification: {certification}\n")
        f.write(f"Topic: {topic}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n" + "=" * 50 + "\n\n")
        f.write(str(crew_result.raw))
    
    return output_filename
