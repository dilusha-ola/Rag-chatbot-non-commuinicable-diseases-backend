"""
Data ingestion module for loading and processing disease information documents.
Supports PDF, TXT, and DOCX files.
"""

import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DataIngestion:
    """Handles loading and processing of disease documents."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data ingestion module.
        
        Args:
            data_dir: Directory containing the disease information files
        """
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def load_pdf_files(self) -> List[Document]:
        """
        Load all PDF files from the data directory.
        
        Returns:
            List of Document objects
        """
        documents = []
        
        try:
            from pypdf import PdfReader
        except ImportError:
            print("PyPDF not installed. Install with: pip install pypdf")
            return documents
        
        if not os.path.exists(self.data_dir):
            print(f"Warning: Data directory '{self.data_dir}' does not exist.")
            return documents
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.data_dir, filename)
                try:
                    reader = PdfReader(file_path)
                    content = ""
                    for page in reader.pages:
                        content += page.extract_text()
                    
                    doc = Document(
                        page_content=content,
                        metadata={"source": filename}
                    )
                    documents.append(doc)
                    print(f"Loaded: {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
        
        return documents
    
    def load_txt_files(self) -> List[Document]:
        """
        Load all TXT files from the data directory.
        
        Returns:
            List of Document objects
        """
        documents = []
        
        if not os.path.exists(self.data_dir):
            print(f"Warning: Data directory '{self.data_dir}' does not exist.")
            return documents
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        doc = Document(
                            page_content=content,
                            metadata={"source": filename}
                        )
                        documents.append(doc)
                        print(f"Loaded: {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
        
        return documents
    
    def load_all_documents(self) -> List[Document]:
        """
        Load all supported document types from the data directory.
        
        Returns:
            List of all Document objects
        """
        all_documents = []
        
        # Load PDF files
        pdf_docs = self.load_pdf_files()
        all_documents.extend(pdf_docs)
        
        # Load text files
        txt_docs = self.load_txt_files()
        all_documents.extend(txt_docs)
        
        print(f"\nTotal documents loaded: {len(all_documents)}")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of split document chunks
        """
        if not documents:
            print("No documents to split.")
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        print(f"Documents split into {len(chunks)} chunks")
        return chunks


if __name__ == "__main__":
    # Example usage
    ingestion = DataIngestion()
    docs = ingestion.load_all_documents()
    chunks = ingestion.split_documents(docs)
    
    if chunks:
        print(f"\nFirst chunk preview:")
        print(chunks[0].page_content[:200])
