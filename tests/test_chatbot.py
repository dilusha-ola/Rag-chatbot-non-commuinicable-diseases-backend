"""
Unit tests for chatbot logic.
Run with: pytest tests/test_chatbot.py
"""

import pytest
from src.chatbot import NCDChatbot
from unittest.mock import Mock, patch, MagicMock


class TestChatbotInitialization:
    """Test chatbot initialization."""
    
    @patch('src.chatbot.VectorStoreManager')
    @patch('src.chatbot.ChatGoogleGenerativeAI')
    @patch('src.chatbot.RetrievalQA')
    def test_chatbot_initialization(self, mock_qa, mock_llm, mock_vector):
        """Test chatbot can be initialized."""
        mock_vector_instance = Mock()
        mock_vector.return_value = mock_vector_instance
        mock_vector_instance.get_retriever.return_value = Mock()
        
        mock_qa.from_chain_type.return_value = Mock()
        
        chatbot = NCDChatbot()
        assert chatbot is not None
        assert hasattr(chatbot, 'qa_chain')


class TestChatbotQueries:
    """Test chatbot query handling."""
    
    @patch('src.chatbot.VectorStoreManager')
    @patch('src.chatbot.ChatGoogleGenerativeAI')
    @patch('src.chatbot.RetrievalQA')
    def test_ask_question_returns_string(self, mock_qa, mock_llm, mock_vector):
        """Test that ask returns a string response."""
        mock_vector_instance = Mock()
        mock_vector.return_value = mock_vector_instance
        mock_vector_instance.get_retriever.return_value = Mock()
        
        mock_chain = Mock()
        mock_chain.invoke.return_value = {"result": "Test answer"}
        mock_qa.from_chain_type.return_value = mock_chain
        
        chatbot = NCDChatbot()
        result = chatbot.ask("What is diabetes?")
        assert isinstance(result, dict)
        assert "answer" in result
        assert isinstance(result["answer"], str)
        assert len(result["answer"]) > 0
    
    @patch('src.chatbot.VectorStoreManager')
    @patch('src.chatbot.ChatGoogleGenerativeAI')
    @patch('src.chatbot.RetrievalQA')
    def test_ask_question_with_empty_input(self, mock_qa, mock_llm, mock_vector):
        """Test chatbot handles empty questions."""
        mock_vector_instance = Mock()
        mock_vector.return_value = mock_vector_instance
        mock_vector_instance.get_retriever.return_value = Mock()
        
        mock_chain = Mock()
        mock_qa.from_chain_type.return_value = mock_chain
        
        chatbot = NCDChatbot()
        result = chatbot.ask("")
        assert isinstance(result, dict)
        assert "answer" in result
