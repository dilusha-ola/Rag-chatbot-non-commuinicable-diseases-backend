# RAG Chatbot for Non-Communicable Diseases

A Retrieval-Augmented Generation (RAG) chatbot that provides information about non-communicable diseases using LangChain, ChromaDB, and OpenAI.

## Features

- 📚 PDF document ingestion and processing
- 🔍 Vector similarity search using ChromaDB
- 🤖 AI-powered responses using OpenAI GPT models
- 💬 Interactive chat interface
- 📊 Source attribution for answers

## Project Structure

```
RAG-Non-communicable-diseases/
├── data/                      # PDF documents about diseases
├── src/
│   ├── data_ingestion.py     # Document loading and chunking
│   ├── vector_store.py       # Vector database management
│   ├── chatbot.py            # RAG chatbot implementation
│   └── setup.py              # Initial setup script
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/dilusha-ola/Rag-chatbot-non-commuinicable-diseases.git
cd Rag-chatbot-non-commuinicable-diseases
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 6. Add Your Documents

Place your PDF files about non-communicable diseases in the `data/` folder.

### 7. Run Setup

This will process your documents and create the vector database:

```bash
python -m src.setup
```

### 8. Run the Chatbot

```bash
python main.py
```

## Usage

Once the chatbot is running, you can ask questions like:

- "What are the symptoms of diabetes?"
- "How can I prevent heart disease?"
- "What are the risk factors for cancer?"
- "Tell me about high blood pressure treatment"

Type `quit`, `exit`, or `q` to end the conversation.

## Technologies Used

- **LangChain**: Framework for building LLM applications
- **ChromaDB**: Vector database for semantic search
- **OpenAI**: GPT models for answer generation and embeddings
- **PyPDF**: PDF document parsing
- **Python-dotenv**: Environment variable management

## How It Works

1. **Document Processing**: PDFs are loaded and split into chunks
2. **Embedding Creation**: Text chunks are converted to vector embeddings
3. **Storage**: Embeddings are stored in ChromaDB
4. **Query Processing**: User questions are converted to embeddings
5. **Retrieval**: Most relevant chunks are found via similarity search
6. **Generation**: GPT generates answers using retrieved context

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for API calls)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub.