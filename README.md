# NCD Health Assistant - Backend

This is the backend server for an AI chatbot that answers questions about non-communicable diseases like diabetes, heart disease, and cancer. It uses your PDF documents as a knowledge base and Google's Gemini AI to provide accurate answers.

## How It Works - High Level View

```
Your Frontend Application
        |
        | (sends questions via HTTP)
        |
        v
FastAPI Backend (this project)
        |
        +---> Reads your question
        |
        +---> Searches through document database
        |     (ChromaDB finds relevant information)
        |
        +---> Sends context to Google Gemini AI
        |
        +---> Returns AI-generated answer


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
└───────┘   └────────────┘```

## Project Structure

```
RAG-Non-communicable-diseases/
├── app.py                  # Main server file
├── src/
│   ├── data_ingestion.py  # Reads and processes PDF files
│   ├── vector_store.py    # Manages the document database
│   ├── chatbot.py         # Handles questions and answers
│   └── setup.py           # Creates the initial database
├── data/                  # Put your PDF documents here
├── chroma_db/            # Database storage (created automatically)
├── setup_backend.bat     # Windows setup script
├── setup_backend.sh      # Mac/Linux setup script
├── start_backend.bat     # Windows start script
├── start_backend.sh      # Mac/Linux start script
├── .env                  # Your configuration and API key
└── requirements.txt      # List of required Python packages
```

## What Does It Do

The backend reads PDF documents about health topics, breaks them into smaller pieces, and stores them in a way that makes searching fast. When someone asks a question, it finds the most relevant information from your documents and uses Google's AI to create a helpful answer.

## What You Need

- Python 3.8 or higher installed on your computer
- A Google API key (you can get one free from Google)
- PDF documents about health topics you want the chatbot to know about

## Getting Started

### For Windows Users

1. Double-click the setup_backend.bat file to install everything automatically

2. Open the .env file and add your Google API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

3. Put your PDF files in the data folder

4. Open Command Prompt in this folder and run:
   ```
   venv\Scripts\activate
   python -m src.setup
   ```

5. Double-click start_backend.bat to start the server

### For Mac or Linux Users

1. Open Terminal in this folder and run:
   ```
   chmod +x setup_backend.sh start_backend.sh
   ./setup_backend.sh
   ```

2. Open the .env file and add your Google API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

3. Put your PDF files in the data folder

4. Run these commands:
   ```
   source venv/bin/activate
   python -m src.setup
   ```

5. Run this to start the server:
   ```
   ./start_backend.sh
   ```

The server will start at http://localhost:8000

You can test it by visiting http://localhost:8000/docs in your browser.

## How to Use the API

The backend provides a simple way for your frontend to ask questions and get answers.

### Main Endpoint

Send a POST request to http://localhost:8000/chat with your question:

```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What are the symptoms of diabetes?'
  })
});
const data = await response.json();
console.log(data.answer);
```

### Check if Server is Running

Visit http://localhost:8000/health to see if everything is working properly.

## Testing

The project includes comprehensive unit and integration tests.

### Running Tests

1. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. Run all tests:
   ```bash
   pytest -v
   ```

3. Run tests with coverage:
   ```bash
   pytest --cov=src --cov=app tests/
   ```

4. Run specific test file:
   ```bash
   pytest tests/test_api.py -v
   ```

### Test Coverage

- **API Endpoints** (`tests/test_api.py`): Tests all REST API endpoints, request/response validation, error handling, and CORS
- **Chatbot Logic** (`tests/test_chatbot.py`): Tests chatbot initialization and question answering
- **Vector Store** (`tests/test_vector_store.py`): Tests document storage and retrieval
- **Integration Tests** (`test_backend.py`): End-to-end tests with running server

### Test Results

All 13 tests should pass:
- 8 API endpoint tests
- 3 chatbot tests
- 2 vector store tests

For more details, see [TESTING.md](TESTING.md)

## API Documentation for Postman Testing

You can test all endpoints using Postman or any HTTP client.

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Root Endpoint
**GET** `/`
- **Description**: Check if API is running
- **Response**:
  ```json
  {
    "status": "ok",
    "message": "NCD RAG Chatbot API is running"
  }
  ```

#### 2. Health Check
**GET** `/health`
- **Description**: Check server and chatbot health
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "Chatbot is ready"
  }
  ```

#### 3. Chat Endpoint (Main)
**POST** `/chat`
- **Description**: Ask a question and get an answer
- **Headers**:
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "question": "What are the symptoms of diabetes?",
    "return_sources": false
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Common symptoms of diabetes include...",
    "sources": null
  }
  ```

#### 4. Chat with Sources
**POST** `/chat`
- **Request Body**:
  ```json
  {
    "question": "What is hypertension?",
    "return_sources": true
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Hypertension, or high blood pressure...",
    "sources": [
      {
        "source": "document.pdf",
        "content": "Relevant excerpt from the document..."
      }
    ]
  }
  ```

#### 5. Interactive API Documentation
**GET** `/docs`
- **Description**: Swagger UI for testing all endpoints in browser
- **URL**: http://localhost:8000/docs

### Postman Collection Setup

1. Create a new collection called "NCD Chatbot API"
2. Set collection variable `baseUrl` = `http://localhost:8000`
3. Add the following requests:

**Request 1: Root**
- Method: GET
- URL: `{{baseUrl}}/`

**Request 2: Health Check**
- Method: GET
- URL: `{{baseUrl}}/health`

**Request 3: Ask Question**
- Method: POST
- URL: `{{baseUrl}}/chat`
- Body (raw JSON):
  ```json
  {
    "question": "What is diabetes?",
    "return_sources": false
  }
  ```

**Request 4: Ask Question with Sources**
- Method: POST
- URL: `{{baseUrl}}/chat`
- Body (raw JSON):
  ```json
  {
    "question": "What causes heart disease?",
    "return_sources": true
  }
  ```

### Error Responses

**400 Bad Request** - Empty question:
```json
{
  "detail": "Question cannot be empty"
}
```

**422 Validation Error** - Missing required field:
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

**500 Internal Server Error** - Processing error:
```json
{
  "detail": "Error processing question: [error message]"
}
```

**503 Service Unavailable** - Vector store not initialized:
```json
{
  "detail": "Vector store not initialized. Please run setup first."
}
```

## Common Issues

**Problem: Server won't start**
Make sure you created the database by running python -m src.setup first.

**Problem: Can't connect from frontend**
Check that the backend is running at http://localhost:8000 and your frontend URL is allowed.

**Problem: Getting errors about missing files**
Make sure you activated the virtual environment before running commands.

## Project Files

- app.py - The main server file
- data folder - Put your PDF documents here
- chroma_db folder - Where the processed documents are stored
- .env file - Your configuration and API key
- src folder - The code that processes documents and generates answers

## Notes

This is just the backend server. You need a separate frontend application to interact with it. The frontend sends questions to this server and displays the answers to users.

The server runs on your computer at port 8000. When you're ready to make it available online, you'll need to deploy it to a hosting service.
