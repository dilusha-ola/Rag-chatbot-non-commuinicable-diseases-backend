"""
FastAPI backend for RAG-based NCD Chatbot.
Provides REST API endpoints for chat functionality.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path to import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot import NCDChatbot

# Initialize FastAPI app
app = FastAPI(
    title="NCD RAG Chatbot API",
    description="RAG-based chatbot for Non-Communicable Diseases information",
    version="1.0.0"
)

# Configure CORS - allow frontend from any origin (configurable via env)
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot instance (singleton)
chatbot_instance = None


def get_chatbot():
    """Get or create chatbot instance."""
    global chatbot_instance
    if chatbot_instance is None:
        try:
            chatbot_instance = NCDChatbot()
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=503,
                detail="Vector store not initialized. Please run setup first."
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize chatbot: {str(e)}"
            )
    return chatbot_instance


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model."""
    question: str
    return_sources: bool = False


class SourceDocument(BaseModel):
    """Source document metadata."""
    source: str
    content: str


class ChatResponse(BaseModel):
    """Chat response model."""
    answer: str
    sources: Optional[List[SourceDocument]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API information."""
    return {
        "status": "ok",
        "message": "NCD RAG Chatbot API is running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Try to get chatbot instance
        get_chatbot()
        return {
            "status": "healthy",
            "message": "Chatbot is ready"
        }
    except HTTPException as e:
        return {
            "status": "unhealthy",
            "message": e.detail
        }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - send a question and get an answer.
    
    Args:
        request: ChatRequest with question and optional return_sources flag
        
    Returns:
        ChatResponse with answer and optional source documents
    """
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        chatbot = get_chatbot()
        response = chatbot.ask(
            question=request.question,
            return_sources=request.return_sources
        )
        
        return ChatResponse(
            answer=response["answer"],
            sources=response.get("sources")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint (for future WebSocket implementation).
    Currently returns same as /chat endpoint.
    """
    return await chat(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
