# Google Sheets Integration - Setup & Testing Guide

## ✅ What's Been Implemented

### 1. Google Sheets Service (`app/services/sheets_service.py`)
- Service account authentication
- Auto-creates worksheet headers if not present
- Appends policy data after verification
- Calculates statistics (record count, average accuracy)
- Graceful error handling (doesn't break verification if Sheets fails)

### 2. Updated Routes
- **Verification Route**: Now saves to both local JSON and Google Sheets
- **Analytics Route**: New `/analytics/sheets` endpoint for Sheets statistics

### 3. Configuration
- **Sheet ID**: `1qI9BbAaIBqg0ES4QEkKBeU_dFJwCCnDyEuQpDwsTp4Q`
- **Sheet Name**: `Database_One`
- **Spreadsheet**: `Totality_Ins_Agency_Records_2026`

---

## 🚀 Setup Steps

### Step 1: Place Service Account Credentials

1. **Download your JSON credentials** from Google Cloud Console
2. **Save it as**: `service-account-dev.json`
3. **Place it in**: `backend/credentials/service-account-dev.json`

```
backend/
├── credentials/
│   ├── service-account-dev.json  ← Your JSON file here
│   ├── README.md
│   └── .gitkeep
```

### Step 2: Verify Configuration

Check your `.env.dev` file has:

```env
GOOGLE_SHEETS_CREDENTIALS_FILE=backend/credentials/service-account-dev.json
GOOGLE_SHEET_ID=1qI9BbAaIBqg0ES4QEkKBeU_dFJwCCnDyEuQpDwsTp4Q
GOOGLE_SHEET_NAME=Database_One
```

### Step 3: Install Dependencies (if needed)

```bash
cd backend
pip install gspread google-auth google-auth-oauthlib
```

(These should already be in `requirements.txt`)

### Step 4: Verify Sheet Permissions

1. Open your Google Sheet
2. Click **Share**
3. **Confirm** the service account email is listed with **Editor** access
   - Email format: `your-service@project-id.iam.gserviceaccount.com`
   - Find this in your JSON credentials file under `"client_email"`

---

## 🧪 Testing

### Test 1: Connection Test

```bash
cd backend
python -c "from app.services.sheets_service import get_sheets_service; service = get_sheets_service(); print('✅ Connected!' if service.connect() else '❌ Failed')"
```

**Expected Output**: `✅ Connected!`

**If it fails**:
- Check credentials file path
- Verify service account email is shared with sheet
- Check internet connection
- Verify Sheet ID is correct

### Test 2: Full Workflow Test

1. **Start the backend**:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

2. **Upload a test PDF**:
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@path/to/your/test.pdf"
```

Save the `file_id` from response.

3. **Extract data**:
```bash
curl -X POST "http://localhost:8000/api/v1/extract/{file_id}"
```

Save the `extraction_id` and `data` from response.

4. **Verify data** (replace with actual values):
```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "extraction_id": "your_extraction_id",
    "verified_data": {
      "policy_number": "TEST123",
      "policy_holder": "John Doe",
      "insurer_name": "Test Insurance",
      "policy_type": "COMP",
      "sum_insured": "1000000",
      "commencing_date": "01/01/2024",
      "expiring_date": "31/12/2024",
      "premium_amount": "50000",
      "paid_amount": "50000",
      "balance_amount": "0"
    },
    "edited_fields": ["premium_amount", "paid_amount"]
  }'
```

5. **Check Google Sheet**: Open your sheet - you should see a new row!

### Test 3: Check Sheets Statistics

```bash
curl http://localhost:8000/api/v1/analytics/sheets
```

**Expected Response**:
```json
{
  "connected": true,
  "total_records": 1,
  "average_accuracy": 75.0,
  "sheet_name": "Database_One",
  "spreadsheet_id": "1qI9BbAaIBqg0ES4QEkKBeU_dFJwCCnDyEuQpDwsTp4Q"
}
```

### Test 4: Interactive API Docs

1. Open: http://localhost:8000/docs
2. Navigate to `/api/v1/verify` endpoint
3. Click **Try it out**
4. Fill in test data
5. Execute
6. Check your Google Sheet for the new row

---

## 📊 Google Sheet Structure

Your sheet will have these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | When record was added | 2026-02-16 14:30:00 |
| Extraction ID | Unique identifier | ext_abc123 |
| Policy Number | Policy number | POL/2024/001 |
| Policy Holder | Name of policy holder | John Doe |
| Insurer Name | Insurance company | AAR Insurance |
| Policy Type | Type of policy | COMP |
| Sum Insured | Coverage amount | 2,000,000 |
| Commencing Date | Start date | 01/01/2024 |
| Expiring Date | End date | 31/12/2024 |
| Premium Amount | Premium paid | 50,000 |
| Paid Amount | Amount paid | 50,000 |
| Balance Amount | Outstanding balance | 0 |
| Accuracy Score (%) | AI accuracy | 75.0 |
| Edited Fields | Fields manually edited | premium_amount, paid_amount |
| Status | Record status | Verified |

---

## 🔧 Troubleshooting

### Error: "Credentials file not found"

**Solution**:
```bash
# Check file exists
ls backend/credentials/service-account-dev.json

# If not, place your JSON file there
# Make sure filename matches exactly: service-account-dev.json
```

### Error: "403 Forbidden" or "Permission denied"

**Solution**:
1. Open your JSON credentials file
2. Find the `"client_email"` field
3. Copy that email address
4. Open your Google Sheet → Share
5. Add that email with **Editor** access

### Error: "Worksheet not found"

**Solution**:
- Check your sheet has a tab named **exactly** "Database_One"
- Or update `GOOGLE_SHEET_NAME` in `.env.dev` to match your actual sheet name

### Error: "Invalid credentials"

**Solution**:
1. Re-download credentials from Google Cloud Console
2. Make sure it's a **Service Account** key (not OAuth)
3. Ensure you downloaded the **JSON** format (not P12)
4. Don't edit the JSON file manually

### Sheets not updating but no errors

**Check**:
1. Backend logs for warnings
2. Verify internet connection
3. Check Google Cloud Console quota (should be way under limits)
4. Try the connection test command above

### Headers not appearing in sheet

**Solution**:
- Delete row 1 in your sheet
- Run a verification request
- Headers will be auto-created

---

## 🎯 What Happens After Verification

1. **Local Storage**: Data saved to `backend/results.json` (backup)
2. **Google Sheets**: Data appended as new row
3. **Response**: User gets accuracy score and success confirmation

If Google Sheets fails, the verification still succeeds (graceful degradation).

---

## 📈 Production Deployment Notes

For production (when deploying to Render/Railway):

1. **Upload credentials to hosting platform**:
   - Render: Environment → Secret Files
   - Railway: Variables → Add file
   
2. **Update `.env.prod`**:
   ```env
   GOOGLE_SHEETS_CREDENTIALS_FILE=/app/credentials/production-credentials.json
   GOOGLE_SHEET_ID=<production_sheet_id>
   GOOGLE_SHEET_NAME=Database_One
   ```

3. **Create separate production sheet**:
   - Don't use the same sheet for dev and prod
   - Share it with the same service account email

---

## ✅ Quick Start Checklist

- [ ] Service account JSON file downloaded
- [ ] File saved as `backend/credentials/service-account-dev.json`
- [ ] Service account email shared with Google Sheet (Editor access)
- [ ] `.env.dev` has correct Sheet ID
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend running (`python -m uvicorn app.main:app --reload`)
- [ ] Connection test passed
- [ ] First test record added successfully
- [ ] Sheet analytics endpoint working

---

## 🎉 Success Indicators

You'll know it's working when:

1. ✅ Connection test prints "Connected!"
2. ✅ After verification, new row appears in Google Sheet
3. ✅ `/analytics/sheets` endpoint returns sheet statistics
4. ✅ No errors in backend console logs
5. ✅ Data in sheet matches verified data

---

## 📞 Need Help?

If you're stuck:

1. **Check backend logs** - Look for error messages
2. **Test connection** - Use the connection test command
3. **Verify permissions** - Service account must have Editor access
4. **Check file paths** - Credentials file must be in correct location
5. **Review environment config** - Sheet ID and name must match exactly

---

## 🚀 Next Steps After Testing

Once Google Sheets integration is working:

1. ✅ **Test with real insurance PDFs**
2. ✅ **Verify data accuracy in sheets**
3. ✅ **Create production sheet** (separate from dev)
4. ⏳ **Create Dockerfile** for backend deployment
5. ⏳ **Deploy to Render/Railway**
6. ⏳ **Deploy frontend to Vercel**
7. ⏳ **Implement calendar reminders** (Phase 4)

You're now ready to test! Let me know if you encounter any issues. 🎯
