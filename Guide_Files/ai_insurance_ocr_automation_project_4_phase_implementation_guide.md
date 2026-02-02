# AI Insurance OCR Automation Project - 4 Phase Implementation Guide

## Project Vision

Build a **simple but highly effective AI-powered system** that:

1. Allows users to upload insurance policy PDFs
2. Uses AI + OCR to extract key insurance variables
3. Allows users to verify and edit extracted data
4. Logs model performance by tracking edits
5. Stores verified data into Google Sheets
6. Automatically generates calendar reminders for policy expiry

---

# High Level System Workflow

User Upload → AI OCR Extraction → User Verification → Store Data → Create Reminder

---

# PHASE 1 — Upload & Extraction Engine

## Objective
Create the user interface and backend pipeline that receives PDFs and extracts structured insurance data using OCR + AI.

---

## User Experience (UX Flow)

1. User opens web interface
2. User uploads insurance policy PDF
3. User presses **Submit**
4. System scans PDF immediately
5. Extracted variables prepared for verification screen

---

## Why Backend Still Receives File First

Even though extraction happens immediately after submit, the backend is required because:

- OCR processing requires server compute
- AI model interaction requires API handling
- File must be temporarily stored for processing
- Backend ensures security and reliability

Frontend = UI interaction
Backend = Processing + AI + Storage control

---

## Tech Stack (Phase 1)

### Frontend
- React (Next.js optional)
- Tailwind CSS
- Axios / Fetch API

### Backend
- Python
- FastAPI
- Pydantic

### OCR + AI Extraction
- Tesseract OCR or Google Document AI
- OpenAI structured extraction

### File Storage (Temporary)
- Local storage during development
- Later upgrade to:
  - Google Cloud Storage
  - AWS S3

---

## Extracted Variables Example

- Client Name
- Policy Number
- Insurer Name
- Sum Insured
- Start Date
- Expiry Date
- Premium Amount
- Policy Type

---

## Learning Goals (Phase 1)

### Backend
- FastAPI architecture
- File upload handling
- REST API design
- Async processing

### AI
- Prompt engineering
- Structured JSON extraction
- OCR pipeline design

### Frontend
- File upload components
- API communication
- State management

---

## GitHub + CI/CD Setup

### Branch Strategy

- main
- develop
- feature/*

### CI Tasks

- Run tests
- Lint code
- Build validation

---

# PHASE 2 — Human Verification + Model Performance Logging

## Objective
Allow users to confirm or edit AI extracted values before saving.

---

## User Experience

1. Extracted data displayed in editable form
2. User edits incorrect fields
3. System tracks:
   - Number of edited fields
   - Fields changed
   - Accuracy score
4. User clicks Confirm & Submit

---

## Performance Logging Logic

Track:

- Total extracted variables
- Variables edited by user
- Accuracy percentage

Formula:

Accuracy = ((Total Fields - Edited Fields) / Total Fields) × 100

---

## Data Flow

AI Output → Editable UI Form → User Edits → Performance Log → Save Verified Data

---

## Tech Stack (Phase 2)

- React Form Libraries (React Hook Form)
- Backend validation
- Logging database or Google Sheet

---

## Learning Goals (Phase 2)

- Controlled forms
- Data validation
- Analytics logging
- UX design

---

# PHASE 3 — Google Sheets Storage + Receipt Generation

## Objective
Store verified policy data and generate client receipts.

---

## User Experience

After submission:

- Policy stored in Google Sheet
- Receipt automatically generated
- Confirmation message displayed

---

## Google Sheets Data Schema

Columns:

- Timestamp
- Client Name
- Policy Number
- Insurer
- Sum Insured
- Start Date
- Expiry Date
- Premium
- Policy Type
- Accuracy Score

---

## Receipt Generation Options

- Google Docs template automation
- PDF receipt creation

---

## Tech Stack (Phase 3)

- Google Sheets API
- Google Docs API
- Python document generation libraries

---

## Learning Goals (Phase 3)

- OAuth authentication
- Google Workspace APIs
- Template automation

---

# PHASE 4 — Automated Reminder System

## Objective
Automatically create expiry reminders.

---

## User Experience

After policy stored:

- Google Calendar reminder created
- Email reminder scheduled

---

## Reminder Logic

Create reminders:

- 30 days before expiry
- 7 days before expiry
- Expiry day

---

## Tech Stack (Phase 4)

- Google Calendar API
- Gmail API
- n8n (optional automation orchestrator)

---

## Learning Goals (Phase 4)

- Event scheduling
- Background job handling
- Automation workflows

---

# Overall Architecture

Frontend (React UI)
↓
Backend API (FastAPI)
↓
OCR + AI Extraction
↓
Verification UI
↓
Google Sheets Storage
↓
Receipt Generation
↓
Reminder Automation

---

# Security Considerations

- Secure file uploads
- Access token storage
- Input validation
- Audit logging

---

# MVP Development Order

1. Upload UI
2. OCR extraction
3. Verification screen
4. Google Sheets storage
5. Reminder automation

---

# Future Enhancements

- Multiple policy upload
- ML model fine-tuning
- Dashboard analytics
- Client portal

---

# Success Metrics

- Extraction accuracy
- User correction rate
- Processing speed
- Reminder reliability

---

# End Goal

A production-ready AI insurance document automation platform that:

- Saves manual data entry time
- Improves policy tracking
- Provides automated reminders
- Generates client documentation

