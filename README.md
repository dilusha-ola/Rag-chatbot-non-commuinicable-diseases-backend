# RAG Chatbot for Non-Communicable Diseases - Backend API

A production-ready FastAPI backend for a Retrieval-Augmented Generation (RAG) chatbot that provides information about non-communicable diseases using LangChain, ChromaDB, and Google Gemini.

## 🏗️ Architecture

This is a **backend-only** repository designed to be consumed by any frontend application (React, Vue, Angular, etc.) via REST API.

```
┌─────────────────┐
│  Your Frontend  │  (Separate Repo)
│   React/Vue/    │
│   Angular/etc   │
└────────┬────────┘
         │ HTTP REST API
         │
┌────────▼────────────┐
│  FastAPI Backend    │  ← This Repository
│  (Port 8000)        │
│  ┌──────────────┐   │
│  │ RAG Pipeline │   │
│  │ + LangChain  │   │
│  └──────────────┘   │
└─────────┬───────────┘
          │
    ┌─────┴──────┐
    │            │
┌───▼───┐   ┌───▼────────┐
│Chroma │   │  Google    │
│Vector │   │  Gemini    │
│  DB   │   │    API     │
└───────┘   └────────────┘
```

## ✨ Features

- 🚀 **FastAPI Backend** - High-performance REST API
- 📚 **PDF Document Processing** - Automatic ingestion and chunking
- 🔍 **Vector Search** - ChromaDB for semantic similarity
- 🤖 **Google Gemini Integration** - Powered by Google's LLM
- 📊 **Source Attribution** - Track information sources
- 🔄 **Auto-reload** - Development mode with hot reload
- 📖 **Interactive Docs** - Swagger UI and ReDoc
- 🌐 **CORS Enabled** - Ready for frontend integration

## 📁 Project Structure

```
RAG-Non-communicable-diseases/
├── app.py                  # FastAPI application
├── src/
│   ├── data_ingestion.py  # Document loading and chunking
│   ├── vector_store.py    # ChromaDB vector database
│   ├── chatbot.py         # RAG chatbot logic
│   └── setup.py           # Database initialization
├── data/                  # Your PDF documents
├── chroma_db/            # Vector database (auto-created)
├── setup_backend.bat     # Windows setup script
├── setup_backend.sh      # Linux/Mac setup script
├── start_backend.bat     # Windows start script
├── start_backend.sh      # Linux/Mac start script
├── test_backend.py       # API test script
├── .env.example         # Environment template
├── requirements.txt     # Dependencies
├── QUICK_START.md      # Quick reference
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))
- PDF documents about non-communicable diseases

### Installation

#### Windows

1. **Run setup:**
   ```bash
   setup_backend.bat
   ```

2. **Configure environment:**
   Edit `.env` file and add your API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Add your documents:**
   Place PDF files in the `data/` folder

4. **Create vector database:**
   ```bash
   venv\Scripts\activate
   python -m src.setup
   ```

5. **Start the server:**
   ```bash
   start_backend.bat
   ```

#### Linux/Mac

1. **Run setup:**
   ```bash
   chmod +x setup_backend.sh start_backend.sh
   ./setup_backend.sh
   ```

2. **Configure environment:**
   Edit `.env` file and add your API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Add your documents:**
   Place PDF files in the `data/` folder

4. **Create vector database:**
   ```bash
   source venv/bin/activate
   python -m src.setup
   ```

5. **Start the server:**
   ```bash
   ./start_backend.sh
   ```

### Access the API

- **API Server**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

---

## � Complete API Reference

### Authentication
Currently no authentication required. Add authentication middleware as needed for production.

### Request/Response Format
All requests and responses use JSON format with `Content-Type: application/json`.

### Endpoints Details

#### 1. Root - GET `/`
Basic API information endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "NCD RAG Chatbot API is running"
}
```

#### 2. Health Check - GET `/health`
Check backend and vector database status.

**Response (Healthy):**
```json
{
  "status": "healthy",
  "message": "Chatbot is ready"
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "message": "Vector store not initialized. Please run setup first."
}
```

#### 3. Chat - POST `/chat`
Main endpoint for asking questions.

**Request Body:**
```json
{
  "question": "string (required)",
  "return_sources": "boolean (optional, default: false)"
}
```

**Response:**
```json
{
  "answer": "string",
  "sources": [
    {
      "source": "filename.pdf",
      "content": "snippet of source text..."
    }
  ]
}
```

**Error Responses:**
- `400` - Invalid or empty question
- `500` - Processing error
- `503` - Vector store not initialized

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are diabetes symptoms?",
    "return_sources": true
  }'
```

**Example with JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What are diabetes symptoms?',
    return_sources: true
  })
});
const data = await response.json();
console.log(data.answer);
data.sources?.forEach(s => console.log(`Source: ${s.source}`));
```

**Example with Python:**
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'question': 'What are diabetes symptoms?',
    'return_sources': True
})

data = response.json()
print(f"Answer: {data['answer']}")
if data.get('sources'):
    for source in data['sources']:
        print(f"Source: {source['source']}")
```

### Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
  - Test endpoints directly in browser
  - View request/response schemas
  - Try out API calls
  
- **ReDoc**: http://localhost:8000/redoc
  - Alternative documentation view
  - Better for reading and reference

---

## �🔌 API Endpoints

### POST `/chat`
Send a question and receive an AI-generated answer.

**Request:**
```json
{
  "question": "What are the symptoms of diabetes?",
  "return_sources": false
}
```

**Response:**
```json
{
  "answer": "Diabetes symptoms include increased thirst, frequent urination...",
  "sources": null
}
```

### GET `/health`
Check if the API is ready.

**Response:**
```json
{
  "status": "healthy",
  "message": "Chatbot is ready"
}
```

📖 **Full API Documentation**: See sections below or visit http://localhost:8000/docs when server is running

---

## 💻 Frontend Integration

This backend is designed to work with **any frontend framework**. Here are quick examples:

### React/Next.js Example

```jsx
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What causes high blood pressure?',
    return_sources: false
  })
});
const data = await response.json();
console.log(data.answer);
```

### Vue.js Example

```javascript
const response = await axios.post('http://localhost:8000/chat', {
  question: 'What causes high blood pressure?',
  return_sources: false
});
console.log(response.data.answer);
```

### Angular Example

```typescript
this.http.post('http://localhost:8000/chat', {
  question: 'What causes high blood pressure?',
  return_sources: false
}).subscribe(data => console.log(data.answer));
```

See examples above for integration with your frontend framework.

---

## 🧪 Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?", "return_sources": true}'
```

### Using Python

```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'question': 'What are the symptoms of high blood pressure?',
    'return_sources': True
})
print(response.json()['answer'])
```

### Using Browser
Visit http://localhost:8000/docs for interactive Swagger UI

---

## 📚 How It Works

1. **Document Ingestion**: PDF documents are loaded from the `data/` folder
2. **Text Chunking**: Documents are split into manageable chunks with overlap
3. **Embedding**: Text chunks are converted to vector embeddings
4. **Storage**: Embeddings are stored in ChromaDB vector database
5. **Query**: User question is embedded and similar chunks are retrieved
6. **Generation**: Google Gemini generates answer based on retrieved context

---

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional
MODEL_NAME=gemini-pro
MODEL_TEMPERATURE=0.7
BACKEND_PORT=8000
RETRIEVAL_K=4
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🐛 Troubleshooting

### Vector store not found
**Solution**: Run `python -m src.setup` to create the database

### CORS errors
**Solution**: Add your frontend URL to `CORS_ORIGINS` in `.env`

### Import errors
**Solution**: Ensure virtual environment is activated

### No response from API
**Solution**: Check if server is running on port 8000

---

## 📦 Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Create vector database
python -m src.setup

# Start server
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

---

## 🚀 Production Deployment

For production environments:

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn backend.app:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

Consider using:
- **Docker** for containerization
- **Nginx** as reverse proxy
- **SSL/TLS** for HTTPS
- **Environment variables** for secrets

---

## 📄 License

MIT License

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check [backend/README.md](backend/README.md) for detailed API docs
- Review the API docs at http://localhost:8000/docs
- Check the QUICK_START.md for common solution
---

## 🎯 Roadmap

- [ ] WebSocket support for streaming responses
- [ ] Multiple LLM provider support
- [ ] Conversation history
- [ ] User authentication
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Docker compose setup

---

**Built with ❤️ using FastAPI, LangChain, ChromaDB, and Google Gemini**
