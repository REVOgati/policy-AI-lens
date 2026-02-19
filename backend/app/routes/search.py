"""
Search route - allows searching Google Sheets records by policy holder, registration number, expiry date (any combination, fuzzy matching).
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional, Dict, Any
from app.services.sheets_service import get_sheets_service
import logging
from datetime import datetime

try:
    from rapidfuzz import fuzz, process
except ImportError:
    fuzz = None
    process = None

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_records(
    policy_holder: Optional[str] = Query(None, description="Policy holder name (Column D)"),
    registration_no: Optional[str] = Query(None, description="Registration number (Column M)"),
    expiry_date: Optional[str] = Query(None, description="Expiry date (DD/MM/YYYY, Column I)"),
):
    """
    Search Google Sheets records by policy holder, registration number, expiry date (any combination).
    Uses fuzzy matching for text fields. Results sorted by latest expiry date.
    """
    sheets_service = get_sheets_service()
    if not sheets_service.connect():
        raise HTTPException(status_code=503, detail="Failed to connect to Google Sheets")

    # Fetch all records (skip header)
    values = sheets_service.worksheet.get_all_values()[1:]
    headers = sheets_service.worksheet.row_values(1)
    results = []

    def normalize(s):
        # Lowercase, remove extra spaces, strip
        return ' '.join(s.lower().split()) if s else ''

    def fuzzy_match(val, query, threshold=70):
        if not query or not val:
            return True
        val_norm = normalize(val)
        query_norm = normalize(query)
        if fuzz:
            # Use token_sort_ratio for better handling of transpositions and spaces
            score = fuzz.token_sort_ratio(val_norm, query_norm)
            return score > threshold
        return query_norm in val_norm

    for row in values:
        record = dict(zip(headers, row))
        matches = []
        if policy_holder:
            # Lower threshold for names to allow more typos
            matches.append(fuzzy_match(record.get('Policy Holder', ''), policy_holder, threshold=65))
        if registration_no:
            # Lower threshold for reg numbers, allow spaces/typos
            matches.append(fuzzy_match(record.get('Registration No', ''), registration_no, threshold=70))
        if expiry_date:
            # Normalize to DD/MM/YYYY
            sheet_date = record.get('Expiring Date', '')
            if sheet_date:
                try:
                    dt = datetime.strptime(sheet_date, "%d/%m/%Y")
                    input_dt = datetime.strptime(expiry_date, "%d/%m/%Y")
                    matches.append(dt == input_dt)
                except Exception:
                    matches.append(sheet_date == expiry_date)
            else:
                matches.append(False)
        if all(matches):
            results.append(record)

    # Sort by Expiring Date (latest first)
    def date_key(rec):
        try:
            return datetime.strptime(rec.get('Expiring Date', ''), "%d/%m/%Y")
        except Exception:
            return datetime.min

    results.sort(key=date_key, reverse=True)
    return results