# Policy AI Lens - Frontend Setup

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

Frontend will start at: http://localhost:5173

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── FileUpload.jsx   # PDF upload component
│   │   ├── VerificationForm.jsx  # Data verification form
│   │   └── LoadingSpinner.jsx    # Loading indicator
│   ├── pages/               # Page components
│   │   ├── UploadPage.jsx   # Upload interface
│   │   └── VerifyPage.jsx   # Verification interface
│   ├── services/            # API integration
│   │   └── api.js           # Backend API calls
│   ├── utils/               # Helper functions
│   ├── App.jsx              # Main app component
│   └── main.jsx             # Entry point
├── public/                  # Static assets
├── package.json             # Dependencies
└── vite.config.js           # Vite configuration
```

## Building Components

### Phase 1: Upload Interface
- File upload component
- Submit button
- Loading state
- Display extracted data

### Phase 2: Verification Form
- Editable form fields
- Track changes
- Submit verified data

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool (fast HMR)
- **Tailwind CSS** - Styling
- **React Hook Form** - Form management
- **Axios** - HTTP client

## API Integration

Backend API: http://localhost:8000/api/v1

See `src/services/api.js` for endpoint methods

## Next Steps

1. Create basic layout
2. Build file upload component
3. Implement extraction display
4. Add verification form
