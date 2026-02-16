"""
Analytics route - provides insights into extraction performance.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from app.services.results_storage import get_results_storage
from app.services.sheets_service import get_sheets_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/analytics/results")
async def get_all_results() -> Dict[str, Any]:
    """
    Get all verification results with summary statistics.

    Returns:
        Dictionary with results and statistics
    """
    storage = get_results_storage()
    results = storage.get_all_results()
    avg_accuracy = storage.get_average_accuracy()

    return {
        "total_verifications": len(results),
        "average_accuracy": avg_accuracy,
        "results": results
    }


@router.get("/analytics/summary")
async def get_summary_stats() -> Dict[str, Any]:
    """
    Get summary statistics only.

    Returns:
        Dictionary with summary metrics
    """
    storage = get_results_storage()
    results = storage.get_all_results()

    if not results:
        return {
            "total_verifications": 0,
            "average_accuracy": 0.0,
            "high_accuracy_count": 0,
            "medium_accuracy_count": 0,
            "low_accuracy_count": 0,
        }

    # Categorize by accuracy
    high = sum(1 for r in results if r.get("accuracy_score", 0) >= 80)
    medium = sum(1 for r in results if 60 <= r.get("accuracy_score", 0) < 80)
    low = sum(1 for r in results if r.get("accuracy_score", 0) < 60)

    # Most commonly edited fields
    all_edited = []
    for r in results:
        all_edited.extend(r.get("edited_fields", []))

    from collections import Counter
    field_counts = Counter(all_edited)
    most_edited = field_counts.most_common(5)

    return {
        "total_verifications": len(results),
        "average_accuracy": storage.get_average_accuracy(),
        "high_accuracy_count": high,
        "medium_accuracy_count": medium,
        "low_accuracy_count": low,
        "most_edited_fields": [{"field": f, "count": c} for f, c in most_edited],
    }


@router.get("/analytics/sheets")
async def get_sheets_stats() -> Dict[str, Any]:
    """
    Get statistics from Google Sheets.
    
    Returns:
        Dictionary with Google Sheets data statistics
    """
    try:
        sheets_service = get_sheets_service()
        
        # Connect to sheets
        if not sheets_service.connect():
            raise HTTPException(
                status_code=503,
                detail="Failed to connect to Google Sheets"
            )
        
        record_count = sheets_service.get_record_count()
        avg_accuracy = sheets_service.get_average_accuracy()
        
        return {
            "connected": True,
            "total_records": record_count,
            "average_accuracy": round(avg_accuracy, 2),
            "sheet_name": sheets_service.settings.google_sheet_name,
            "spreadsheet_id": sheets_service.settings.google_sheet_id
        }
        
    except Exception as e:
        logger.error(f"Failed to get Google Sheets stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve Google Sheets statistics: {str(e)}"
        )
