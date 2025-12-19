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
