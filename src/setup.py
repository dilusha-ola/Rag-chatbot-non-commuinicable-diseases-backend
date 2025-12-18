"""
Setup script to initialize the RAG system.
Loads documents and creates the vector store.
"""

import os
from dotenv import load_dotenv
from src.data_ingestion import DataIngestion
from src.vector_store import VectorStoreManager


def main():
    """
    Main setup function to prepare the RAG system.
    """
    print("=" * 70)
    print("RAG Chatbot Setup - Non-Communicable Diseases")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Check if Google API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n❌ Error: GOOGLE_API_KEY not found in .env file")
        print("Please add your Google Gemini API key to the .env file")
        return
    
    print("\n✓ Environment variables loaded")
    
    # Step 1: Load and process documents
    print("\n" + "=" * 70)
    print("Step 1: Loading and processing documents")
    print("=" * 70)
    
    ingestion = DataIngestion(data_dir="data")
    documents = ingestion.load_all_documents()
    
    if not documents:
        print("\n❌ No documents found in the 'data' directory")
        print("Please add PDF or TXT files to the 'data' directory")
        return
    
    print(f"\n✓ Loaded {len(documents)} documents")
    
    # Step 2: Split documents into chunks
    print("\n" + "=" * 70)
    print("Step 2: Splitting documents into chunks")
    print("=" * 70)
    
    chunks = ingestion.split_documents(documents)
    
    if not chunks:
        print("\n❌ Failed to split documents")
        return
    
    print(f"\n✓ Created {len(chunks)} document chunks")
    
    # Step 3: Create vector store
    print("\n" + "=" * 70)
    print("Step 3: Creating vector store (this may take a few minutes)")
    print("=" * 70)
    
    try:
        vs_manager = VectorStoreManager()
        vs_manager.create_vector_store(chunks)
        print("\n✓ Vector store created successfully")
    except Exception as e:
        print(f"\n❌ Error creating vector store: {str(e)}")
        return
    
    # Success
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print("\nYou can now run the chatbot using:")
    print("  python -m src.chatbot")
    print("\nOr import and use it in your code:")
    print("  from src.chatbot import NCDChatbot")
    print("  chatbot = NCDChatbot()")
    print("  chatbot.chat()")


if __name__ == "__main__":
    main()
