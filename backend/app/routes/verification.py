"""
Verification route - handles user verification and performance tracking.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import VerificationRequest, VerificationResponse
from app.services.results_storage import get_results_storage
from app.services.sheets_service import get_sheets_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


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
        # Calculate accuracy score with conditional field evaluation
        # Fields always excluded: premium_amount, paid_amount, balance_amount (never in PDFs)
        excluded_fields = {'premium_amount', 'paid_amount', 'balance_amount'}
        
        # Check policy type for conditional sum_insured evaluation
        policy_type = request.verified_data.policy_type or ""
        is_comprehensive = 'COMP' in policy_type.upper()
        
        # If not comprehensive, sum_insured is always null (should not affect accuracy)
        if not is_comprehensive:
            excluded_fields.add('sum_insured')
            total_fields = 6  # 10 total - 4 excluded (premium, paid, balance, sum_insured)
        else:
            total_fields = 7  # 10 total - 3 excluded (premium, paid, balance)
        
        # Filter edited fields to only include fields used for accuracy
        accuracy_edited_fields = [
            field for field in request.edited_fields 
            if field not in excluded_fields
        ]
        
        edited_count = len(accuracy_edited_fields)
        accuracy = ((total_fields - edited_count) / total_fields) * 100 if total_fields > 0 else 100.0

        # Save result for analytics (use accuracy_edited_fields, not all)
        storage = get_results_storage()
        storage.save_result(
            extraction_id=request.extraction_id,
            policy_number=request.verified_data.policy_number,
            accuracy_score=accuracy,
            edited_fields=accuracy_edited_fields
        )

        # Phase 3: Save to Google Sheets
        try:
            sheets_service = get_sheets_service()
            sheets_success = sheets_service.append_policy_data(
                extraction_id=request.extraction_id,
                policy_data=request.verified_data.model_dump(),
                accuracy_score=accuracy,
                edited_fields=accuracy_edited_fields,
                status="Verified"
            )
            
            if not sheets_success:
                logger.warning(
                    f"Failed to save to Google Sheets for extraction {request.extraction_id}"
                )
        except Exception as sheets_error:
            # Log error but don't fail the verification
            logger.error(f"Google Sheets error: {sheets_error}")
            # Continue - local storage already succeeded

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
        ) from e
