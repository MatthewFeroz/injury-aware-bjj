#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints work correctly
"""
import requests
import json

def test_api():
    base_url = "http://localhost:5000"  # Change this to your deployed URL
    
    # Test recommendations endpoint
    print("Testing /api/recommendations...")
    try:
        response = requests.post(f"{base_url}/api/recommendations", 
                               json={"injuries": ["knee injury"]},
                               headers={"Content-Type": "application/json"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            print("✅ Recommendations endpoint working")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test chat endpoint
    print("\nTesting /api/chat...")
    try:
        response = requests.post(f"{base_url}/api/chat",
                               json={"message": "Hello, I have a knee injury"},
                               headers={"Content-Type": "application/json"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            print("✅ Chat endpoint working")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_api()
