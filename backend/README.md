# Policy AI Lens - Backend

## 🎯 Overview
AI-powered insurance policy data extraction system using **Google Gemini Vision API** to automatically extract structured data from insurance policy PDFs.

## ✨ Features
- 📄 **PDF Upload**: Upload insurance policy documents
- 🤖 **AI Extraction**: Gemini Vision directly processes PDFs (no OCR needed!)
- ✅ **Verification**: Human review and editing of extracted data
- 📊 **Accuracy Tracking**: Calculates AI extraction accuracy
- 🔧 **Debug Tools**: OCR fallback for testing and debugging

## 🚀 Current Status
✅ **Phase 1 Complete**: Backend extraction pipeline fully functional
- Upload endpoint working
- Gemini Vision extraction working (75% accuracy)
- Verification endpoint working
- Complete workflow tested

⏳ **Next**: Frontend UI development (Phase 2)

---

## 🛠️ Technology Stack
- **Framework**: FastAPI 0.109.0 (async)
- **AI Model**: Google Gemini Vision (gemini-2.5-flash)
- **PDF Processing**: PyMuPDF (fitz) + PIL for image conversion
- **Backup OCR**: Tesseract OCR + Poppler (for debugging)
- **Validation**: Pydantic V2
- **Environment**: Python 3.11+

---

## 📦 Installation

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

**Windows:**
- Download installer: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location: `C:\Program Files\Tesseract-OCR`
### 2. Install Tesseract OCR (Optional - for debugging only)

**Windows:**
- Download installer: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location: `C:\Program Files\Tesseract-OCR`

**Linux:**
```bash
sudo apt update && sudo apt install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

**Note**: Main extraction uses Gemini Vision. Tesseract is only needed for the debug OCR endpoint.

### 3. Get Google Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

### 4. Configure Environment

```bash
# Navigate to envs directory
cd envs

# Copy example file
cp .env.example .env.dev

# Edit .env.dev and add your API key
```

Required environment variables:
```env
GEMINI_API_KEY=your_actual_api_key_here
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows only
```

### 5. Run the Server

```bash
# Activate virtual environment
policy_venv\Scripts\activate  # Windows
# source policy_venv/bin/activate  # Linux/Mac

# Run server
python -m app.main
```

Server starts at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings & environment config
│   ├── routes/              # API endpoints
│   │   ├── upload.py        # PDF upload
│   │   ├── extraction.py    # Gemini Vision extraction
│   │   └── verification.py  # Human verification
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # Gemini Vision AI (main)
│   │   └── ocr_service.py   # Legacy OCR (debug only)
│   └── models/
│       └── schemas.py       # Pydantic data models
├── envs/
│   ├── .env.dev             # Development config
│   └── .env.example         # Example config file
├── tests/                   # Test scripts
├── uploads/                 # Uploaded PDFs storage
└── requirements.txt         # Dependencies
```

---

## 🧪 Testing

### Complete Workflow Test
```bash
# Run complete end-to-end test
python tests/test_complete_flow.py
```

Expected output:
- ✅ Upload working
- ✅ Extraction working (Gemini Vision)
- ✅ Verification working
- 📊 Accuracy: ~75% (6/8 fields)

### Manual Testing
1. Open http://localhost:8000/docs
2. Upload a PDF using `/api/v1/upload`
3. Use returned `file_id` in `/api/v1/extract/{file_id}`
4. Review extracted data
5. Submit verified data to `/api/v1/verify`

### Debug Tools
```bash
# Test Gemini Vision extraction
python tests/test_gemini_vision.py

# View raw OCR output (debugging)
curl http://localhost:8000/api/v1/debug/ocr/{file_id}
```

---

## 📊 Performance

**Current Extraction Accuracy**: ~75%
- ✅ Policy Holder: Extracted
- ✅ Policy Number: Extracted
- ✅ Insurer Name: Extracted
- ✅ Commencing Date: Extracted
- ✅ Expiring Date: Extracted
- ✅ Policy Type: Extracted
- ⚠️  Sum Insured: Often N/A (manual entry)
- ⚠️  Premium Amount: Not on certificates (manual entry)

**Processing Time**: 2-5 seconds per PDF
**Supported Format**: PDF only
**Max File Size**: 10MB

---

## 🔧 Troubleshooting

### Gemini API Quota Exceeded
```
Error: 429 You exceeded your current quota
```
**Solution**: 
- Wait for quota reset (per-minute or daily limits)
- System auto-tries multiple models with available quota
- Free tier: 1500 requests/day per model

### Extraction Returns Null Values
**Normal for**:
- Motor Third Party certificates (no sum_insured)
- Certificates vs full policies (missing dates/premium)

**Solution**: Users add during verification step

### Server Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process using port (Windows)
taskkill /PID <PID> /F

# Restart server
python -m app.main
```

### Tesseract Errors (Debug Endpoint Only)
**Note**: Main extraction doesn't need Tesseract
- Only affects `/api/v1/debug/ocr/{file_id}` endpoint
- Install Tesseract if you need this endpoint
- Otherwise, safely ignore

---

## 📚 API Documentation

Full API documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

Or visit interactive docs: http://localhost:8000/docs

---

## 🎯 Next Steps

1. **Frontend Development** (Phase 2)
   - React UI for upload
   - Verification form with editable fields
   - Real-time accuracy display

2. **Google Sheets Integration** (Phase 3)
   - OAuth authentication
   - Automatic data storage
   - Sheet creation/updating

3. **Calendar Reminders** (Phase 4)
   - Expiry date tracking
   - Automated notifications

---

## 🤝 Contributing

This is a learning project. Feel free to:
- Test with different insurance policies
- Suggest improvements
- Report bugs via GitHub Issues
- Check `uploads/` directory exists
- Verify file size limits (10MB default)
- Ensure PDF format

## Next Steps

1. Test with sample insurance PDF
2. Adjust AI prompt in `ai_service.py` if needed
3. Build frontend UI (see frontend/ directory)
4. Integrate Google Sheets (Phase 3)
