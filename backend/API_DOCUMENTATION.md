# Policy AI Lens - API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## API Endpoints

### 1. Health Check
#### `GET /`
Check if the API is running.

**Response:**
```json
{
  "message": "Policy AI Lens API",
  "version": "0.1.0",
  "status": "running"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. Upload PDF
#### `POST /api/v1/upload`
Upload an insurance policy PDF for processing.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file, max 10MB)

**Response (200 OK):**
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "file_id": "9589b490-9df7-4481-9683-cbd951288a41",
  "filename": "insurance_policy.pdf"
}
```

**Errors:**
- `400`: Only PDF files allowed or file size exceeds limit
- `500`: Server error

---

### 3. Extract Policy Data
#### `POST /api/v1/extract/{file_id}`
Extract structured data from uploaded PDF using Gemini Vision AI.

**Parameters:**
- `file_id` (path): UUID of uploaded file

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Policy data extracted successfully using Gemini Vision",
  "data": {
    "policy_holder": "SHARLYNE NEKESA CHEPTOO",
    "policy_number": "G/010/0700/1008681/2025",
    "insurer_name": "Trident Insurance Company Ltd.",
    "sum_insured": null,
    "commencing_date": "17/11/2024",
    "expiring_date": "16/12/2025",
    "premium_amount": null,
    "policy_type": "Motor Third Party"
  },
  "extraction_id": "9589b490-9df7-4481-9683-cbd951288a41"
}
```

**Extracted Fields:**
- `policy_holder`: Name of the policy holder
- `policy_number`: Unique policy identifier
- `insurer_name`: Insurance company name
- `sum_insured`: Coverage amount (often null for Motor Third Party)
- `commencing_date`: Policy start date (DD/MM/YYYY)
- `expiring_date`: Policy end date (DD/MM/YYYY)
- `premium_amount`: Premium amount (often needs manual entry)
- `policy_type`: Type of insurance (Motor Third Party, Comprehensive, etc.)

**Errors:**
- `404`: File not found
- `500`: Extraction failed

---

### 4. Verify Policy Data
#### `POST /api/v1/verify`
Submit verified policy data after human review and editing.

**Request Body:**
```json
{
  "extraction_id": "9589b490-9df7-4481-9683-cbd951288a41",
  "verified_data": {
    "policy_holder": "SHARLYNE NEKESA CHEPTOO",
    "policy_number": "G/010/0700/1008681/2025",
    "insurer_name": "Trident Insurance Company Ltd.",
    "sum_insured": "N/A",
    "commencing_date": "17/11/2024",
    "expiring_date": "16/12/2025",
    "premium_amount": "5500",
    "policy_type": "Motor Third Party"
  },
  "edited_fields": ["premium_amount", "sum_insured"]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Policy data verified and saved",
  "accuracy_score": 75.0,
  "total_fields": 8,
  "edited_fields_count": 2
}
```

**Errors:**
- `500`: Verification failed

---

### 5. Debug OCR Text (Optional)
#### `GET /api/v1/debug/ocr/{file_id}`
View raw OCR text extracted from PDF (for debugging purposes).

**Parameters:**
- `file_id` (path): UUID of uploaded file

**Response (200 OK):**
```json
{
  "success": true,
  "file_id": "9589b490-9df7-4481-9683-cbd951288a41",
  "text_length": 1749,
  "raw_text": "Full extracted text here...",
  "preview": "First 1000 characters..."
}
```

**Note:** This endpoint uses legacy OCR (PyMuPDF + Tesseract) for debugging. Main extraction uses Gemini Vision.

---

## Complete Workflow

### Step 1: Upload PDF
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@policy.pdf"
```

### Step 2: Extract Data
```bash
curl -X POST "http://localhost:8000/api/v1/extract/{file_id}"
```

### Step 3: Verify & Save
```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "extraction_id": "file_id_here",
    "verified_data": {...},
    "edited_fields": ["premium_amount"]
  }'
```

---

## Technologies Used

- **AI Model**: Google Gemini Vision (gemini-2.5-flash)
- **PDF Processing**: PyMuPDF (fitz), Pillow for image conversion
- **Backup OCR**: Tesseract OCR, Poppler for legacy support
- **Framework**: FastAPI with async/await
- **Validation**: Pydantic V2

---

## Performance Metrics

- **Extraction Accuracy**: ~75% (6/8 fields extracted automatically)
- **Processing Time**: ~2-5 seconds per PDF (depending on model and quota)
- **Supported Formats**: PDF only
- **Max File Size**: 10MB
- **Free Tier Quota**: 1500 requests/day (Gemini API)

---

## Next Steps (Future Phases)

- **Phase 3**: Google Sheets integration for data storage
- **Phase 4**: Automated calendar reminders based on expiry dates
- **Frontend**: React UI for upload, review, and verification
