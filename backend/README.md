# Policy AI Lens - Backend Setup

## Quick Start

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
- Add to PATH if needed

**Linux:**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

### 3. Get Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy the key

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Server

```bash
# Make sure you're in the backend directory with venv activated
cd backend
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload
```

Server will start at: http://localhost:8000

### 6. Test the API

Open browser: http://localhost:8000/docs

You'll see interactive API documentation (Swagger UI)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── routes/              # API endpoints
│   │   ├── upload.py        # File upload
│   │   ├── extraction.py    # OCR + AI extraction
│   │   └── verification.py  # Data verification
│   ├── services/            # Business logic
│   │   ├── ocr_service.py   # OCR processing
│   │   └── ai_service.py    # Gemini AI integration
│   ├── models/              # Data models
│   │   └── schemas.py       # Pydantic schemas
│   └── utils/               # Helper functions
├── uploads/                 # Temporary file storage
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## API Endpoints

### 1. Health Check
```
GET /
GET /health
```

### 2. Upload PDF
```
POST /api/v1/upload
Body: multipart/form-data with PDF file
```

### 3. Extract Policy Data
```
POST /api/v1/extract/{file_id}
Returns: Extracted policy data
```

### 4. Verify & Save
```
POST /api/v1/verify
Body: {
  "extraction_id": "uuid",
  "verified_data": { ... },
  "edited_fields": ["field1", "field2"]
}
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Troubleshooting

### Tesseract not found
- Windows: Check path in .env file
- Ensure Tesseract is installed and in PATH

### Gemini API errors
- Verify API key is correct
- Check rate limits (1500 requests/day on free tier)
- Ensure good internet connection

### File upload errors
- Check `uploads/` directory exists
- Verify file size limits (10MB default)
- Ensure PDF format

## Next Steps

1. Test with sample insurance PDF
2. Adjust AI prompt in `ai_service.py` if needed
3. Build frontend UI (see frontend/ directory)
4. Integrate Google Sheets (Phase 3)
