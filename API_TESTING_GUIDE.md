# API Testing Guide - Postman & cURL

This guide shows you how to test the NCD Chatbot API using Postman and cURL.

## Quick Start

### Server URL
```
http://localhost:8000
```

Make sure the backend server is running before testing!

---

## Using Postman

### Method 1: Import Collection (Recommended)

1. Open Postman
2. Click **Import** button
3. Select `NCD_Chatbot_API.postman_collection.json` from this directory
4. The collection "NCD Chatbot API" will be added with all endpoints ready to test
5. Click on any request and hit **Send**

### Method 2: Manual Setup

1. Create a new collection called "NCD Chatbot API"
2. Add a collection variable:
   - Variable: `baseUrl`
   - Value: `http://localhost:8000`
3. Add requests as shown below

---

## API Endpoints

### 1. Check API Status

**GET** `http://localhost:8000/`

**Postman Steps:**
1. Create new request
2. Method: GET
3. URL: `{{baseUrl}}/`
4. Click Send

**Expected Response:**
```json
{
  "status": "ok",
  "message": "NCD RAG Chatbot API is running"
}
```

---

### 2. Health Check

**GET** `http://localhost:8000/health`

**Postman Steps:**
1. Method: GET
2. URL: `{{baseUrl}}/health`
3. Click Send

**Expected Response (Healthy):**
```json
{
  "status": "healthy",
  "message": "Chatbot is ready"
}
```

**Expected Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "message": "Vector store not initialized. Please run setup first."
}
```

---

### 3. Ask a Question (Basic)

**POST** `http://localhost:8000/chat`

**Postman Steps:**
1. Method: POST
2. URL: `{{baseUrl}}/chat`
3. Headers:
   - Key: `Content-Type`
   - Value: `application/json`
4. Body → raw → JSON:
```json
{
  "question": "What is diabetes?",
  "return_sources": false
}
```
5. Click Send

**Expected Response:**
```json
{
  "answer": "Diabetes is a chronic metabolic disorder characterized by elevated blood glucose levels...",
  "sources": null
}
```

---

### 4. Ask a Question (With Sources)

**POST** `http://localhost:8000/chat`

**Postman Steps:**
1. Method: POST
2. URL: `{{baseUrl}}/chat`
3. Headers: `Content-Type: application/json`
4. Body:
```json
{
  "question": "What are the symptoms of diabetes?",
  "return_sources": true
}
```
5. Click Send

**Expected Response:**
```json
{
  "answer": "Common symptoms of diabetes include increased thirst, frequent urination...",
  "sources": [
    {
      "source": "diabetes_guide.pdf",
      "content": "Excerpt from the document..."
    }
  ]
}
```

---

### 5. Error Testing - Empty Question

**POST** `http://localhost:8000/chat`

**Body:**
```json
{
  "question": "",
  "return_sources": false
}
```

**Expected Response (400):**
```json
{
  "detail": "Question cannot be empty"
}
```

---

### 6. Error Testing - Missing Field

**POST** `http://localhost:8000/chat`

**Body:**
```json
{
  "return_sources": false
}
```

**Expected Response (422):**
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

---

## Using cURL

### 1. Check API Status
```bash
curl http://localhost:8000/
```

### 2. Health Check
```bash
curl http://localhost:8000/health
```

### 3. Ask a Question (Basic)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is diabetes?\", \"return_sources\": false}"
```

### 4. Ask a Question (With Sources)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are the symptoms of diabetes?\", \"return_sources\": true}"
```

### 5. Pretty Print JSON Response
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is hypertension?\", \"return_sources\": true}" \
  | python -m json.tool
```

---

## Windows PowerShell Examples

### Ask a Question
```powershell
$body = @{
    question = "What is diabetes?"
    return_sources = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json"
```

### Ask Question with Sources
```powershell
$body = @{
    question = "What are the risk factors for heart disease?"
    return_sources = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json"
```

---

## Testing Checklist

### Basic Functionality
- [ ] GET / returns status "ok"
- [ ] GET /health returns "healthy" status
- [ ] POST /chat with valid question returns answer
- [ ] POST /chat with return_sources=true returns sources array

### Error Handling
- [ ] Empty question returns 400 error
- [ ] Missing question field returns 422 error
- [ ] Invalid JSON returns 422 error

### Sample Questions to Test
- [ ] "What is diabetes?"
- [ ] "What are the symptoms of diabetes?"
- [ ] "What causes heart disease?"
- [ ] "What is hypertension?"
- [ ] "How can I prevent cancer?"
- [ ] "What are the risk factors for stroke?"

---

## Postman Tests (Optional)

You can add automated tests to your Postman requests:

### Test 1: Status Code
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

### Test 2: Response Structure
```javascript
pm.test("Response has required fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('answer');
    pm.expect(jsonData.answer).to.be.a('string');
});
```

### Test 3: Response Time
```javascript
pm.test("Response time is less than 5000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(5000);
});
```

### Test 4: Sources Included
```javascript
pm.test("Sources are included when requested", function () {
    var jsonData = pm.response.json();
    if (pm.request.body.raw.includes('"return_sources": true')) {
        pm.expect(jsonData).to.have.property('sources');
    }
});
```

---

## Interactive Documentation

Visit these URLs in your browser for interactive testing:

### Swagger UI
```
http://localhost:8000/docs
```
- Try out endpoints directly in the browser
- See request/response schemas
- Download OpenAPI specification

### ReDoc
```
http://localhost:8000/redoc
```
- Alternative documentation format
- Better for reading and understanding

---

## Troubleshooting

### Issue: Connection Refused
**Solution**: Make sure the backend server is running
```bash
cd RAG-Non-communicable-diseases
venv\Scripts\activate  # Windows
python -m uvicorn app:app --reload
```

### Issue: 503 Service Unavailable
**Solution**: Initialize the vector database
```bash
python -m src.setup
```

### Issue: Slow Response
**Cause**: First request initializes models (can take 10-30 seconds)
**Solution**: Subsequent requests will be faster

### Issue: CORS Error (from browser)
**Solution**: Already configured for localhost:3000 and localhost:5173
Check `CORS_ORIGINS` in .env file if using different port

---

## Advanced Testing

### Load Testing with Apache Bench
```bash
# Install Apache Bench (ab)
# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 -p question.json -T application/json http://localhost:8000/chat
```

**question.json:**
```json
{"question": "What is diabetes?", "return_sources": false}
```

### Testing with Python
```python
import requests

# Test endpoint
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "question": "What is diabetes?",
        "return_sources": True
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

---

## Environment Variables for Testing

Create different environments in Postman:

### Local Development
- `baseUrl`: `http://localhost:8000`

### Staging
- `baseUrl`: `https://staging.yourapp.com`

### Production
- `baseUrl`: `https://api.yourapp.com`

---

## Summary

1. **Import the Postman collection** for instant testing
2. **Use Swagger UI** at `/docs` for interactive testing
3. **Start with basic endpoints** (/, /health)
4. **Test chat endpoint** with sample questions
5. **Verify error handling** with invalid inputs
6. **Check response times** and sources

Happy Testing! 🚀
