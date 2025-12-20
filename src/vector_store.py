"""
Vector store module for managing ChromaDB vector database.
Handles document embedding and similarity search.
"""

import os
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStoreManager:
    """Manages ChromaDB vector store for document retrieval."""
    
    def __init__(
        self,
        persist_directory: str = "chroma_db",
        collection_name: str = "ncd_diseases"
    ):
        """
        Initialize the vector store manager.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Use free HuggingFace embeddings
        print("Loading embedding model (this may take a moment on first run)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create a new vector store from documents.
        
        Args:
            documents: List of document chunks to embed
            
        Returns:
            Chroma vector store instance
        """
        if not documents:
            raise ValueError("No documents provided to create vector store.")
        
        print(f"Creating vector store with {len(documents)} documents...")
        
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        
        print(f"Vector store created and persisted to '{self.persist_directory}'")
        return self.vector_store
    
    def load_vector_store(self) -> Chroma:
        """
        Load an existing vector store from disk.
        
        Returns:
            Chroma vector store instance
        """
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(
                f"Vector store directory '{self.persist_directory}' not found. "
                "Please create the vector store first."
            )
        
        print(f"Loading vector store from '{self.persist_directory}'...")
        
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )
        
        print("Vector store loaded successfully")
        return self.vector_store
    
    def similarity_search(
        self,
        query: str,
        k: int = 4
    ) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of most similar documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Load or create one first.")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add new documents to an existing vector store.
        
        Args:
            documents: List of document chunks to add
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Load it first.")
        
        if not documents:
            print("No documents to add.")
            return
        
        print(f"Adding {len(documents)} new document chunks to vector store...")
        self.vector_store.add_documents(documents)
        print("Documents added successfully")
    
    def get_existing_sources(self) -> List[str]:
        """
        Get list of source filenames already in the vector store.
        
        Returns:
            List of source filenames
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Load it first.")
        
        # Get all documents and extract unique sources
        collection = self.vector_store._collection
        all_metadata = collection.get()['metadatas']
        sources = set()
        
        for metadata in all_metadata:
            if metadata and 'source' in metadata:
                sources.add(metadata['source'])
        
        return sorted(list(sources))
    
    def get_retriever(self, search_kwargs: dict = None):
        """
        Get a retriever instance for use in chains.
        
        Args:
            search_kwargs: Optional search parameters (e.g., {"k": 4})
            
        Returns:
            Retriever instance
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Load or create one first.")
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize vector store manager
    vs_manager = VectorStoreManager()
    
    # Try to load existing store
    try:
        vs_manager.load_vector_store()
        
        # Test similarity search
        query = "What are the symptoms of diabetes?"
        results = vs_manager.similarity_search(query, k=3)
        
        print(f"\nSearch results for: '{query}'")
        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc.metadata.get('source', 'Unknown')}")
            print(doc.page_content[:200])
    except FileNotFoundError:
        print("No existing vector store found. Please run the setup pipeline first.")
