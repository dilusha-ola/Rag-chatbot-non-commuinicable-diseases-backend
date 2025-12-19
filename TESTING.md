# Testing Guide

This project includes comprehensive tests for both backend and frontend.

## Backend Testing

### What's Tested

- API endpoints (root, health, chat)
- Request/response validation
- Error handling
- CORS configuration
- Vector store functionality
- Chatbot logic

### Running Backend Tests

1. Make sure your virtual environment is activated:
   ```
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
   ```

2. Install test dependencies:
   ```
   pip install pytest pytest-cov httpx
   ```

3. Run all tests:
   ```
   pytest
   ```

4. Run tests with coverage:
   ```
   pytest --cov=src --cov=app tests/
   ```

5. Run specific test file:
   ```
   pytest tests/test_api.py
   ```

6. Run with verbose output:
   ```
   pytest -v
   ```

### Backend Test Files

- `tests/test_api.py` - API endpoint tests
- `tests/test_chatbot.py` - Chatbot functionality tests
- `tests/test_vector_store.py` - Vector database tests
- `test_backend.py` - Integration test script (requires running server)

### Running Integration Tests

These tests require the server to be running:

1. Start the backend server:
   ```
   Windows: start_backend.bat
   Mac/Linux: ./start_backend.sh
   ```

2. In another terminal, run:
   ```
   python test_backend.py
   ```

## Frontend Testing

### What's Tested

- API service calls and error handling
- Component rendering and interactions
- User input validation
- Chat history management
- Local storage persistence
- Button clicks and form submissions

### Running Frontend Tests

1. Navigate to frontend folder:
   ```
   cd my-chatbot-ui
   ```

2. Run all tests:
   ```
   npm test
   ```

3. Run tests with UI (interactive):
   ```
   npm run test:ui
   ```

4. Run tests with coverage:
   ```
   npm run test:coverage
   ```

5. Run tests in watch mode:
   ```
   npm test -- --watch
   ```

### Frontend Test Files

- `src/tests/api.test.ts` - API service tests
- `src/tests/ChatInput.test.tsx` - Chat input component tests
- `src/tests/ChatHistory.test.tsx` - Chat history component tests
- `src/tests/storage.test.ts` - Local storage tests
- `src/tests/setup.ts` - Test configuration

## Test Coverage

### Backend
- API endpoints: Complete
- Error handling: Complete
- Request validation: Complete
- CORS: Basic

### Frontend
- API integration: Complete
- Components: Core components covered
- User interactions: Complete
- Storage: Complete

## Common Issues

**Backend: ModuleNotFoundError**
Make sure virtual environment is activated.

**Frontend: Cannot find module vitest**
Run `npm install` to install dependencies.

**Tests failing due to missing server**
Integration tests need the backend server running.

**Test timeout errors**
Increase timeout in test configuration or check server is responsive.

## Writing New Tests

### Backend Example
```python
def test_new_feature():
    response = client.get("/new-endpoint")
    assert response.status_code == 200
```

### Frontend Example
```typescript
it('should do something', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Continuous Integration

Both test suites are designed to work with CI/CD pipelines. Make sure to:
- Run backend tests before deployment
- Check test coverage meets your requirements
- Run frontend tests on pull requests
