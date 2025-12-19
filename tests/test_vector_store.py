"""
Unit tests for vector store operations.
Run with: pytest tests/test_vector_store.py
"""

import pytest
from unittest.mock import Mock, patch
from src.vector_store import VectorStoreManager


class TestVectorStoreManager:
    """Test vector store manager."""
    
    @patch('src.vector_store.Chroma')
    def test_vector_store_initialization(self, mock_chroma):
        """Test vector store can be initialized."""
        mock_chroma.return_value = Mock()
        manager = VectorStoreManager()
        assert manager is not None
    
    @patch('src.vector_store.Chroma')
    def test_get_retriever_returns_retriever(self, mock_chroma):
        """Test get_retriever returns a retriever object."""
        mock_db = Mock()
        mock_chroma.return_value = mock_db
        mock_db.as_retriever.return_value = Mock()
        
        manager = VectorStoreManager()
        manager.vector_store = mock_db  # Set the vector store directly
        retriever = manager.get_retriever()
        assert retriever is not None
        mock_db.as_retriever.assert_called_once()
