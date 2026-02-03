"""
Quick API Testing Script
Run this to understand how the backend works
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("POLICY AI LENS - API TEST")
print("=" * 60)

# Test 1: Health Check
print("\n[1] Testing Health Check...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Root Endpoint
print("\n[2] Testing Root Endpoint...")
response = requests.get(f"{BASE_URL}/")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Upload PDF (will need actual PDF)
print("\n[3] PDF Upload Test")
print("To test upload, you need a PDF file.")
print("Example code:")
print("""
with open('sample_policy.pdf', 'rb') as f:
    files = {'file': ('policy.pdf', f, 'application/pdf')}
    response = requests.post(f'{BASE_URL}/api/v1/upload', files=files)
    print(response.json())
""")

print("\n" + "=" * 60)
print("API is running! Next: Let's understand each component")
print("=" * 60)
