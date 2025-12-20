"""
Script to add new documents to existing vector store.
Only processes documents that haven't been added yet.
"""

import os
from dotenv import load_dotenv
from src.data_ingestion import DataIngestion
from src.vector_store import VectorStoreManager


def main():
    """
    Add new documents to the existing vector store.
    """
    print("=" * 70)
    print("Add New Documents to Vector Store")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Step 1: Load vector store
    print("\n" + "=" * 70)
    print("Step 1: Loading existing vector store")
    print("=" * 70)
    
    try:
        vs_manager = VectorStoreManager()
        vs_manager.load_vector_store()
        print("✓ Vector store loaded")
    except FileNotFoundError:
        print("\n❌ No existing vector store found!")
        print("Please run 'python src/setup.py' first to create the initial vector store")
        return
    
    # Step 2: Get existing sources
    print("\n" + "=" * 70)
    print("Step 2: Checking existing documents")
    print("=" * 70)
    
    existing_sources = vs_manager.get_existing_sources()
    print(f"Found {len(existing_sources)} existing document(s) in vector store:")
    for source in existing_sources:
        print(f"  - {source}")
    
    # Step 3: Load all documents from data directory
    print("\n" + "=" * 70)
    print("Step 3: Scanning data directory for new documents")
    print("=" * 70)
    
    ingestion = DataIngestion(data_dir="data")
    all_documents = ingestion.load_all_documents()
    
    if not all_documents:
        print("\n❌ No documents found in the 'data' directory")
        return
    
    # Step 4: Filter out documents that already exist
    new_documents = []
    for doc in all_documents:
        source = doc.metadata.get('source', '')
        if source not in existing_sources:
            new_documents.append(doc)
    
    if not new_documents:
        print("\n✓ No new documents to add. All files are already in the vector store!")
        return
    
    print(f"\nFound {len(new_documents)} new document(s) to process:")
    for doc in new_documents:
        print(f"  - {doc.metadata.get('source', 'Unknown')}")
    
    # Step 5: Split new documents into chunks
    print("\n" + "=" * 70)
    print("Step 4: Processing new documents")
    print("=" * 70)
    
    chunks = ingestion.split_documents(new_documents)
    
    if not chunks:
        print("\n❌ Failed to split documents")
        return
    
    print(f"✓ Created {len(chunks)} document chunks from new files")
    
    # Step 6: Add to vector store
    print("\n" + "=" * 70)
    print("Step 5: Adding to vector store")
    print("=" * 70)
    
    try:
        vs_manager.add_documents(chunks)
        print("\n✓ New documents added successfully!")
    except Exception as e:
        print(f"\n❌ Error adding documents: {str(e)}")
        return
    
    # Success
    print("\n" + "=" * 70)
    print("Update Complete!")
    print("=" * 70)
    
    # Show updated sources
    updated_sources = vs_manager.get_existing_sources()
    print(f"\nVector store now contains {len(updated_sources)} document(s):")
    for source in updated_sources:
        print(f"  - {source}")


if __name__ == "__main__":
    main()
