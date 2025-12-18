"""
Test script to verify the backend API is working correctly.
Run this after starting the server with start_backend.bat/sh
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    print("\nTesting / endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chat():
    """Test the chat endpoint."""
    print("\nTesting /chat endpoint...")
    test_question = "What is diabetes?"
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "question": test_question,
                "return_sources": True
            }
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Question: {test_question}")
        print(f"Answer: {data.get('answer', 'No answer')[:200]}...")
        
        if data.get('sources'):
            print(f"Sources found: {len(data['sources'])}")
            for i, source in enumerate(data['sources'][:2], 1):
                print(f"  Source {i}: {source.get('source', 'Unknown')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 70)
    print("NCD Chatbot Backend API Test")
    print("=" * 70)
    print(f"\nTesting API at: {BASE_URL}")
    print("\nMake sure the server is running (start_backend.bat/sh)\n")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("Chat Endpoint", test_chat()))
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✓ All tests passed! Backend is working correctly.")
        return 0
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
