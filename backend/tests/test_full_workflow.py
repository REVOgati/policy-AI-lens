"""
COMPLETE WORKFLOW TEST - Upload → Extract → Verify
Run this to test the full pipeline
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 70)
print("FULL WORKFLOW TEST: Upload → OCR → AI Extraction → Verification")
print("=" * 70)

# Step 1: Upload PDF
print("\n📤 STEP 1: Upload PDF")
print("-" * 70)

# You need to provide a PDF file path here
PDF_PATH = input("Enter path to your insurance policy PDF (or press Enter to skip): ").strip()

if not PDF_PATH:
    print("⚠️  No PDF provided. Please add a PDF to test the full workflow.")
    print("\nTo test manually:")
    print("1. Go to http://localhost:8000/docs")
    print("2. Find POST /api/v1/upload")
    print("3. Upload a PDF file")
    print("4. Copy the 'file_id' from response")
    print("5. Use it in POST /api/v1/extract/{file_id}")
    exit()

try:
    # Upload the PDF
    with open(PDF_PATH, 'rb') as f:
        files = {'file': (PDF_PATH.split('\\')[-1], f, 'application/pdf')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        exit()
    
    upload_result = response.json()
    print(f"✅ Upload successful!")
    print(f"   File ID: {upload_result['file_id']}")
    print(f"   Filename: {upload_result['filename']}")
    
    file_id = upload_result['file_id']
    
    # Step 2: Extract Policy Data
    print("\n🔍 STEP 2: Extract Policy Data (OCR + AI)")
    print("-" * 70)
    print("⏳ Processing... (this may take 10-30 seconds)")
    
    response = requests.post(f"{BASE_URL}/extract/{file_id}")
    
    if response.status_code != 200:
        print(f"❌ Extraction failed: {response.text}")
        exit()
    
    extraction_result = response.json()
    print(f"✅ Extraction successful!")
    print("\n📋 EXTRACTED DATA:")
    print(json.dumps(extraction_result['data'], indent=2))
    
    # Step 3: Simulate User Verification
    print("\n✏️  STEP 3: User Verification")
    print("-" * 70)
    print("In real app, user would edit fields in a form.")
    print("For demo, we'll simulate editing 2 fields:\n")
    
    # Simulate user editing some fields
    verified_data = extraction_result['data']
    edited_fields = []
    
    # Example: User might correct policy holder and policy number
    print(f"Original Policy Holder: {verified_data.get('policy_holder')}")
    new_name = input("Enter corrected name (or press Enter to keep): ").strip()
    if new_name:
        verified_data['policy_holder'] = new_name
        edited_fields.append('policy_holder')
    
    print(f"\nOriginal Policy Number: {verified_data.get('policy_number')}")
    new_policy = input("Enter corrected policy number (or press Enter to keep): ").strip()
    if new_policy:
        verified_data['policy_number'] = new_policy
        edited_fields.append('policy_number')
    
    # Step 4: Submit Verification
    print("\n💾 STEP 4: Submit Verified Data")
    print("-" * 70)
    
    verification_payload = {
        "extraction_id": file_id,
        "verified_data": verified_data,
        "edited_fields": edited_fields
    }
    
    response = requests.post(f"{BASE_URL}/verify", json=verification_payload)
    
    if response.status_code != 200:
        print(f"❌ Verification failed: {response.text}")
        exit()
    
    verification_result = response.json()
    print(f"✅ Verification complete!")
    print(f"\n📊 ACCURACY METRICS:")
    print(f"   Accuracy Score: {verification_result['accuracy_score']}%")
    print(f"   Total Fields: {verification_result['total_fields']}")
    print(f"   Edited Fields: {verification_result['edited_fields_count']}")
    print(f"   Edited: {', '.join(edited_fields) if edited_fields else 'None'}")
    
    print("\n" + "=" * 70)
    print("✅ WORKFLOW COMPLETE!")
    print("=" * 70)
    print("\n📝 Summary:")
    print(f"   1. Uploaded: {upload_result['filename']}")
    print(f"   2. Extracted: {len([v for v in verified_data.values() if v])} fields found")
    print(f"   3. Verified: {verification_result['accuracy_score']}% accuracy")
    print(f"   4. Next: Phase 3 will save to Google Sheets")

except FileNotFoundError:
    print(f"❌ File not found: {PDF_PATH}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
