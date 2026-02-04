"""
Test script for Gemini Vision direct PDF extraction
"""
import requests
import os
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

# Find a test PDF
UPLOADS_DIR = "uploads"
pdf_files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith('.pdf')]

if not pdf_files:
    print("❌ No PDF files found in uploads/ directory")
    print("Please upload a PDF first using the upload endpoint or Swagger UI")
    exit(1)

# Use the first PDF found (or most recent)
test_file = pdf_files[-1]  # Get last uploaded
file_id = test_file.replace('.pdf', '')

print("=" * 70)
print("🧪 TESTING GEMINI VISION DIRECT EXTRACTION")
print("=" * 70)
print(f"📄 Using file: {test_file}")
print(f"🆔 File ID: {file_id}")
print("=" * 70)

# Test the extraction endpoint
print("\n1️⃣ Testing extraction with Gemini Vision...")
print("-" * 70)

try:
    response = requests.post(f"{BASE_URL}/extract/{file_id}")

    if response.status_code == 200:
        result = response.json()
        print("✅ Extraction successful!")
        print("\n📊 EXTRACTED DATA:")
        print(json.dumps(result, indent=2))

        # Show extracted fields
        data = result.get('data', {})
        print("\n📋 FIELD VALUES:")
        print("-" * 70)
        for field, value in data.items():
            status = "✅" if value else "❌"
            print(f"{status} {field:20s}: {value}")

    else:
        print(f"❌ Extraction failed with status code: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("🏁 Test completed!")
print("=" * 70)
