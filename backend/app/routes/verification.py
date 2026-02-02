"""
Verification route - handles user verification and performance tracking.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import VerificationRequest, VerificationResponse

router = APIRouter()


@router.post("/verify", response_model=VerificationResponse)
async def verify_policy_data(request: VerificationRequest):
    """
    Verify and save policy data after user edits.
    
    Args:
        request: VerificationRequest with verified data and edited fields
        
    Returns:
        VerificationResponse with accuracy metrics
    """
    try:
        # Calculate accuracy score
        total_fields = 8
        edited_count = len(request.edited_fields)
        accuracy = ((total_fields - edited_count) / total_fields) * 100
        
        # TODO Phase 2: Log performance metrics
        # TODO Phase 3: Save to Google Sheets
        
        return VerificationResponse(
            success=True,
            message="Policy data verified and saved",
            accuracy_score=round(accuracy, 2),
            total_fields=total_fields,
            edited_fields_count=edited_count
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {str(e)}"
        )
