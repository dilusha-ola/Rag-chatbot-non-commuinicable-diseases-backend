# NCD Health Assistant - Complete Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Features](#features)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [API Reference](#api-reference)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Development](#development)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

The NCD Health Assistant is a full-stack Retrieval-Augmented Generation (RAG) application designed to answer questions about Non-Communicable Diseases (NCDs) such as diabetes, heart disease, cancer, and hypertension. The system uses PDF documents as a knowledge base and leverages Google's Gemini AI to provide accurate, context-aware responses.

### Key Capabilities

- ✅ Document ingestion from PDF files
- ✅ Vector-based semantic search
- ✅ AI-powered question answering
- ✅ Source attribution and citations
- ✅ RESTful API with CORS support
- ✅ Comprehensive test coverage
- ✅ Interactive API documentation

---

## Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11.3 | Core programming language |
| **FastAPI** | 0.115.0 | Modern web framework for building APIs |
| **Uvicorn** | 0.32.0 | ASGI server for running FastAPI |
| **LangChain** | 1.2.0 | Framework for LLM applications |
| **ChromaDB** | 1.3.7 | Vector database for embeddings |
| **Google Gemini** | Latest | Large Language Model (LLM) |
| **Sentence Transformers** | Latest | Text embedding models |
| **PyPDF** | 5.2.0 | PDF document processing |
| **Pydantic** | 2.10.0 | Data validation and settings |
| **Python-dotenv** | 1.2.1 | Environment variable management |

### Testing

| Technology | Version | Purpose |
|------------|---------|---------|
| **Pytest** | 8.3.3 | Testing framework |
| **Pytest-cov** | 4.1.0 | Code coverage reporting |
| **HTTPX** | 0.27.0 | Async HTTP client for testing |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19.2.0 | UI library |
| **TypeScript** | 5.9.3 | Type-safe JavaScript |
| **Vite** | 7.2.4 | Build tool and dev server |
| **Tailwind CSS** | 4.1.18 | Utility-first CSS framework |
| **Vitest** | 4.0.16 | Testing framework |
| **React Testing Library** | 16.3.1 | Component testing |

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Application                  │
│              (React + TypeScript + Vite)                │
│                  Port: 5173 (dev)                       │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ HTTP REST API (JSON)
                  │ CORS Enabled
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  FastAPI Backend                        │
│                    Port: 8000                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │           RAG Pipeline (LangChain)               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌───────────┐  │  │
│  │  │  Document  │→ │   Vector   │→ │ Retrieval │  │  │
│  │  │  Ingestion │  │   Store    │  │     QA    │  │  │
│  │  └────────────┘  └────────────┘  └───────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────┬──────────────────────────┬────────────────────┘
          │                          │
          │                          │
┌─────────▼──────────┐    ┌─────────▼──────────────┐
│   ChromaDB         │    │   Google Gemini API    │
│   Vector Database  │    │   (gemini-1.5-flash)   │
│   (Local Storage)  │    │   (Cloud Service)      │
└────────────────────┘    └────────────────────────┘
```

### RAG Pipeline Flow

```
1. Document Ingestion
   ├── Load PDF files from data/ directory
   ├── Extract text using PyPDF
   ├── Split into chunks (1000 chars, 200 overlap)
   └── Generate embeddings using HuggingFace

2. Vector Store
   ├── Store embeddings in ChromaDB
   ├── Create searchable index
   └── Persist to disk (chroma_db/)

3. Question Processing
   ├── Receive question via API
   ├── Generate question embedding
   ├── Similarity search in vector store
   ├── Retrieve top-k relevant chunks
   └── Pass to LLM with context

4. Answer Generation
   ├── LLM processes question + context
   ├── Generate coherent answer
   ├── Include source attribution
   └── Return via API
```

### Directory Structure

```
RAG-Non-communicable-diseases/          # Backend Repository
├── app.py                              # FastAPI application entry point
├── main.py                             # Alternative entry point
├── requirements.txt                    # Python dependencies
├── requirements-test.txt               # Testing dependencies
├── pytest.ini                          # Pytest configuration
├── .env                                # Environment variables (API keys)
├── .gitignore                          # Git ignore rules
│
├── src/                                # Source code modules
│   ├── __init__.py
│   ├── setup.py                        # Database initialization script
│   ├── data_ingestion.py               # PDF processing and chunking
│   ├── vector_store.py                 # ChromaDB management
│   └── chatbot.py                      # RAG chatbot implementation
│
├── tests/                              # Unit tests
│   ├── __init__.py
│   ├── test_api.py                     # API endpoint tests
│   ├── test_chatbot.py                 # Chatbot logic tests
│   └── test_vector_store.py            # Vector store tests
│
├── data/                               # PDF documents storage
│   └── README.md                       # Instructions for adding PDFs
│
├── chroma_db/                          # Vector database (auto-generated)
│   ├── chroma.sqlite3
│   └── [embeddings data]
│
├── docs/                               # Documentation
│   ├── README.md
│   ├── TESTING.md
│   ├── DOCUMENTATION.md
│   └── QUICK_START.md
│
└── scripts/                            # Utility scripts
    ├── setup_backend.bat               # Windows setup
    ├── setup_backend.sh                # Unix setup
    ├── start_backend.bat               # Windows start
    └── start_backend.sh                # Unix start

my-chatbot-ui/                          # Frontend Repository
├── package.json                        # Node dependencies
├── vite.config.ts                      # Vite configuration
├── tsconfig.json                       # TypeScript config
├── tailwind.config.js                  # Tailwind CSS config
├── vitest.config.ts                    # Vitest config
│
├── src/
│   ├── App.tsx                         # Main application component
│   ├── main.tsx                        # Application entry point
│   ├── index.css                       # Global styles
│   │
│   ├── components/                     # React components
│   │   ├── ChatMessage.tsx             # Message display
│   │   ├── ChatInput.tsx               # Input component
│   │   ├── ChatHistory.tsx             # Message history
│   │   └── ReferencePanel.tsx          # Source citations
│   │
│   ├── services/                       # API services
│   │   └── api.ts                      # Backend API client
│   │
│   ├── types/                          # TypeScript types
│   │   └── chat.ts                     # Chat-related types
│   │
│   ├── utils/                          # Utility functions
│   │   └── storage.ts                  # LocalStorage helpers
│   │
│   └── tests/                          # Component tests
│       ├── setup.ts                    # Test configuration
│       ├── ChatMessage.test.tsx
│       ├── ChatInput.test.tsx
│       ├── ChatHistory.test.tsx
│       ├── api.test.ts
│       └── storage.test.ts
│
└── public/                             # Static assets
```

---

## Features

### Backend Features

#### 1. Document Processing
- PDF parsing and text extraction
- Intelligent text chunking with overlap
- Support for multiple document formats
- Batch document ingestion

#### 2. Vector Search
- Semantic similarity search
- Efficient embedding storage
- Persistent vector database
- Configurable retrieval parameters

#### 3. AI-Powered Responses
- Context-aware answer generation
- Source attribution and citations
- Streaming response support (planned)
- Multi-turn conversation support (planned)

#### 4. REST API
- OpenAPI/Swagger documentation
- Request/response validation
- Comprehensive error handling
- CORS configuration for frontend

#### 5. Testing & Quality
- 13 comprehensive unit tests
- Integration test suite
- Code coverage reporting
- Automated CI/CD (planned)

### Frontend Features

#### 1. User Interface
- Clean, modern chat interface
- Responsive design (mobile/desktop)
- Message history
- Loading states and animations

#### 2. Chat Features
- Real-time message display
- Source reference panel
- Message persistence
- Clear chat functionality

#### 3. Testing
- Component unit tests
- API service tests
- User interaction tests
- Storage utility tests

---

## Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher (for frontend)
- **Git**: Latest version
- **Google API Key**: From Google AI Studio

### Backend Setup

#### Windows

```batch
# Clone repository
git clone <repository-url>
cd RAG-Non-communicable-diseases

# Run automated setup
setup_backend.bat

# Configure environment
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Add PDF documents
# Place your PDF files in the data/ folder

# Initialize database
venv\Scripts\activate
python -m src.setup

# Start server
start_backend.bat
```

#### Mac/Linux

```bash
# Clone repository
git clone <repository-url>
cd RAG-Non-communicable-diseases

# Make scripts executable
chmod +x setup_backend.sh start_backend.sh

# Run automated setup
./setup_backend.sh

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Add PDF documents
# Place your PDF files in the data/ folder

# Initialize database
source venv/bin/activate
python -m src.setup

# Start server
./start_backend.sh
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd my-chatbot-ui

# Install dependencies
npm install

# Configure API URL (if needed)
# Edit src/services/api.ts

# Start development server
npm run dev

# Build for production
npm run build
```

---

## Configuration

### Environment Variables

Create a `.env` file in the backend root:

```env
# Required: Google API Key
GOOGLE_API_KEY=your_google_api_key_here

# Optional: CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional: Server Configuration
HOST=0.0.0.0
PORT=8000

# Optional: Model Configuration
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.7
MAX_TOKENS=2048

# Optional: Vector Store Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
COLLECTION_NAME=ncd_documents
```

### Pytest Configuration

`pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

#### GET /

**Description**: Root endpoint, API status check

**Response**: `200 OK`
```json
{
  "status": "ok",
  "message": "NCD RAG Chatbot API is running"
}
```

---

#### GET /health

**Description**: Health check endpoint

**Response**: `200 OK` (healthy) or `503 Service Unavailable` (unhealthy)
```json
{
  "status": "healthy",
  "message": "Chatbot is ready"
}
```

---

#### POST /chat

**Description**: Ask a question and receive an AI-generated answer

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "question": "What are the symptoms of diabetes?",
  "return_sources": false
}
```

**Response**: `200 OK`
```json
{
  "answer": "Common symptoms of diabetes include increased thirst, frequent urination, extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores, and frequent infections.",
  "sources": null
}
```

**With Sources** (`return_sources: true`):
```json
{
  "answer": "Common symptoms of diabetes include...",
  "sources": [
    {
      "source": "diabetes_guide.pdf",
      "content": "Diabetes symptoms include increased thirst (polydipsia)..."
    }
  ]
}
```

**Error Responses**:

`400 Bad Request`:
```json
{
  "detail": "Question cannot be empty"
}
```

`422 Unprocessable Entity`:
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

`500 Internal Server Error`:
```json
{
  "detail": "Error processing question: [error message]"
}
```

`503 Service Unavailable`:
```json
{
  "detail": "Vector store not initialized. Please run setup first."
}
```

---

#### GET /docs

**Description**: Interactive API documentation (Swagger UI)

**URL**: http://localhost:8000/docs

---

#### GET /redoc

**Description**: Alternative API documentation (ReDoc)

**URL**: http://localhost:8000/redoc

---

## Testing

### Backend Testing

#### Test Structure

```
tests/
├── test_api.py           # 8 tests - API endpoints
├── test_chatbot.py       # 3 tests - Chatbot logic
└── test_vector_store.py  # 2 tests - Vector store
```

#### Running Tests

```bash
# Activate environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_api.py::TestAPIEndpoints

# Run specific test
pytest tests/test_api.py::TestAPIEndpoints::test_chat_endpoint_with_valid_question

# Run with coverage
pytest --cov=src --cov=app tests/

# Generate HTML coverage report
pytest --cov=src --cov=app --cov-report=html tests/
```

#### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| `app.py` | 8 | High |
| `src/chatbot.py` | 3 | High |
| `src/vector_store.py` | 2 | Medium |
| `src/data_ingestion.py` | - | Low |

**Total**: 13 tests, all passing

#### Integration Testing

```bash
# Start the server in one terminal
python -m uvicorn app:app --reload

# Run integration tests in another terminal
python test_backend.py
```

### Frontend Testing

```bash
cd my-chatbot-ui

# Run all tests
npm test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run specific test file
npm test ChatMessage.test.tsx
```

#### Frontend Test Coverage

| Component/Service | Tests | Status |
|-------------------|-------|--------|
| `ChatMessage.tsx` | 5+ | ✅ Pass |
| `ChatInput.tsx` | 5+ | ✅ Pass |
| `ChatHistory.tsx` | 5+ | ✅ Pass |
| `api.ts` | 5+ | ✅ Pass |
| `storage.ts` | 5+ | ✅ Pass |

---

## Deployment

### Backend Deployment

#### Option 1: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set GOOGLE_API_KEY=your_key_here

# Deploy
railway up
```

#### Option 2: Render

1. Connect GitHub repository
2. Select "Web Service"
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GOOGLE_API_KEY`

#### Option 3: Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t ncd-chatbot-backend .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key ncd-chatbot-backend
```

### Frontend Deployment

#### Option 1: Vercel

```bash
npm install -g vercel
vercel
```

#### Option 2: Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

---

## Development

### Adding New Features

#### Backend

1. Create feature branch
2. Implement in `src/` modules
3. Add API endpoint in `app.py`
4. Write tests in `tests/`
5. Update documentation
6. Submit PR

#### Frontend

1. Create component in `src/components/`
2. Add types in `src/types/`
3. Write tests in `src/tests/`
4. Update README
5. Submit PR

### Code Style

**Backend**: PEP 8 (Python)
```bash
# Install formatters
pip install black flake8

# Format code
black .

# Lint code
flake8 .
```

**Frontend**: ESLint + Prettier
```bash
# Lint
npm run lint

# Format
npm run format
```

---

## Troubleshooting

### Common Issues

#### Backend

**Issue**: `ModuleNotFoundError: No module named 'src'`
```bash
# Solution: Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**Issue**: `Vector store not initialized`
```bash
# Solution: Run setup script
python -m src.setup
```

**Issue**: `CORS error from frontend`
```bash
# Solution: Update CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Issue**: Tests failing with `AttributeError: module 'app' has no attribute 'chatbot'`
```bash
# Solution: Tests are now fixed to mock get_chatbot function
# Pull latest changes
```

#### Frontend

**Issue**: `Failed to fetch` error
```bash
# Solution: Ensure backend is running on port 8000
# Check src/services/api.ts for correct API URL
```

**Issue**: Build fails
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## License

This project is licensed under the MIT License.

---

## Support

For issues, questions, or contributions:
- GitHub Issues: [Create an issue]
- Documentation: See README.md and TESTING.md
- API Docs: http://localhost:8000/docs

---

## Changelog

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ RAG pipeline implementation
- ✅ FastAPI backend
- ✅ React frontend
- ✅ Comprehensive testing
- ✅ Documentation

### Upcoming Features
- 🔄 Streaming responses
- 🔄 Multi-turn conversations
- 🔄 User authentication
- 🔄 Chat history persistence
- 🔄 Advanced analytics
