# 🚀 Quick Reference - NCD Chatbot Backend

## One-Time Setup

```bash
# Windows
setup_backend.bat

# Linux/Mac
chmod +x *.sh
./setup_backend.sh
```

Then:
1. Edit `.env` - add your `GOOGLE_API_KEY`
2. Add PDFs to `data/` folder
3. Run: `python -m src.setup` (creates vector DB)

---

## Start Server

```bash
# Windows
start_backend.bat

# Linux/Mac
./start_backend.sh
```

Server runs on: **http://localhost:8000**

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/chat` | POST | Ask questions |
| `/docs` | GET | Swagger UI |
| `/redoc` | GET | ReDoc docs |

---

## Test the API

```bash
# After starting server
python test_backend.py
```

Or visit: http://localhost:8000/docs

---

## Quick cURL Test

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is diabetes?\", \"return_sources\": false}"
```

---

## Frontend Integration

### React/Next.js
```javascript
const res = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'What is diabetes?', return_sources: false })
});
const data = await res.json();
```

### Vue.js/Nuxt
```javascript
const { data } = await axios.post('http://localhost:8000/chat', {
  question: 'What is diabetes?',
  return_sources: false
});
```

### Angular
```typescript
this.http.post('http://localhost:8000/chat', {
  question: 'What is diabetes?',
  return_sources: false
}).subscribe(data => console.log(data));
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Vector store not found | Run `python -m src.setup` |
| CORS errors | Add frontend URL to `.env` CORS_ORIGINS |
| Import errors | Activate venv: `venv\Scripts\activate` |
| Server won't start | Check port 8000 is free |
| No API key | Add GOOGLE_API_KEY to `.env` |

---

## File Structure

```
project/
├── app.py           # FastAPI application
├── src/             # RAG logic
│   ├── chatbot.py   # RAG chain
│   ├── vector_store.py
│   ├── data_ingestion.py
│   └── setup.py
├── data/            # Your PDFs
├── .env             # Your config (create from .env.example)
└── README.md        # Main docs
```

---

## Environment Variables

```env
GOOGLE_API_KEY=your_key_here          # Required
MODEL_NAME=gemini-pro                 # Optional
MODEL_TEMPERATURE=0.7                 # Optional
CORS_ORIGINS=http://localhost:3000    # Optional
```

---

## Documentation

- **Main README**: [README.md](README.md)
- **API Docs**: [backend/README.md](backend/README.md)
- **Swagger UI**: http://localhost:8000/docs (when running)
- **ReDoc**: http://localhost:8000/redoc (when running)
Quick Start**: This file
---

**Need help?** Check [backend/README.md](backend/README.md) for complete documentation.
