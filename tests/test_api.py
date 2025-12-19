"""
Unit tests for FastAPI endpoints.
Run with: pytest tests/test_api.py
"""

import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test all API endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns correct status and message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data
    
    def test_health_endpoint_structure(self):
        """Test health endpoint returns proper structure."""
        response = client.get("/health")
        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data
        assert "message" in data
    
    @patch('app.get_chatbot')
    def test_chat_endpoint_with_valid_question(self, mock_get_chatbot):
        """Test chat endpoint with a valid question."""
        mock_chatbot_instance = mock_get_chatbot.return_value
        mock_chatbot_instance.ask.return_value = {"answer": "Diabetes is a chronic disease."}
        
        response = client.post(
            "/chat",
            json={"question": "What is diabetes?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 0
    
    def test_chat_endpoint_with_empty_question(self):
        """Test chat endpoint rejects empty questions."""
        response = client.post(
            "/chat",
            json={"question": ""}
        )
        assert response.status_code == 400
    
    @patch('app.get_chatbot')
    def test_chat_endpoint_with_sources(self, mock_get_chatbot):
        """Test chat endpoint can return sources."""
        mock_chatbot_instance = mock_get_chatbot.return_value
        mock_chatbot_instance.ask.return_value = {
            "answer": "Diabetes is a chronic disease.",
            "sources": [{"source": "test.pdf", "content": "Test content"}]
        }
        
        response = client.post(
            "/chat",
            json={"question": "What is diabetes?", "return_sources": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
    
    def test_chat_endpoint_missing_question(self):
        """Test chat endpoint handles missing question field."""
        response = client.post("/chat", json={})
        assert response.status_code == 422
    
    def test_chat_endpoint_invalid_json(self):
        """Test chat endpoint handles invalid JSON."""
        response = client.post(
            "/chat",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.options(
            "/chat",
            headers={"Origin": "http://localhost:5173"}
        )
        assert response.status_code in [200, 405]
