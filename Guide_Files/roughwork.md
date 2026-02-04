# Premium, Paid - Revealed at verification stage before submission ; Not part of logging (verifying AI consistency)
# Balance - calculated after Premium - Paid (Abstracted) - Google sheet side

# Option to directly share from whatsapp into platform (Apk for Android)

--------------------------------------
Frontend Game Plan - User Flow
Phase 2: Verification UI (What we're building now)
User Journey:
Step 1: Upload PDF

User lands on homepage
Drag & drop zone OR click to browse
File validation (PDF only, max 10MB)
Upload progress indicator
Success: Get file_id, move to extraction
Step 2: AI Extraction (Loading State)

Show "Analyzing document..." with spinner
Call /api/v1/extract/{file_id}
Processing time: ~2-5 seconds
Display extracted data when ready
Step 3: Verification Form

Left side: Original extracted data (read-only preview)
Right side: Editable form with 8 fields:
✅ Policy Holder (auto-filled)
✅ Policy Number (auto-filled)
✅ Insurer Name (auto-filled)
⚠️ Sum Insured (often null - user adds)
✅ Commencing Date (auto-filled)
✅ Expiring Date (auto-filled)
⚠️ Premium Amount (often null - user adds)
✅ Policy Type (auto-filled)
Visual indicators:
Green checkmark = AI extracted
Yellow warning = Needs manual entry
Track which fields user edits
Step 4: Submit & Results

Submit button → Call /api/v1/verify
Show success message with:
✅ Accuracy score (e.g., "AI extracted 6/8 fields correctly - 75%")
List of fields that needed editing
Option to:
Upload another policy
View/export data (future: Google Sheets)
Key Features:
Single Page App (SPA)

Upload → Extract → Verify flow on one page
Smooth transitions between steps
Real-time Validation

Required fields highlighted
Date format validation (DD/MM/YYYY)
Number validation for amounts
User Feedback

Loading states for all async operations
Error messages if extraction fails
Success animations
Responsive Design

Works on desktop (primary)
Mobile-friendly for review
Tech Stack (Already Initialized):
✅ React 18 + TypeScript
✅ Vite (dev server)
✅ Tailwind CSS (styling)
React Hook Form (form state)
Axios (API calls)
Component Structure:
User Experience Goals:
⚡ Fast: Upload to results in < 10 seconds
🎯 Simple: 3 clear steps (Upload → Review → Submit)
✨ Helpful: Show what AI extracted vs what needs manual entry
📊 Transparent: Display accuracy to build trust
