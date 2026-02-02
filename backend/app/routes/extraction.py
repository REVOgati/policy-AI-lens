"""
Extraction route - handles OCR and AI extraction.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ExtractionResponse
from app.services.ocr_service import extract_text_from_pdf
from app.services.ai_service import extract_policy_data
from app.config import get_settings
import os

router = APIRouter()
settings = get_settings()


@router.post("/extract/{file_id}", response_model=ExtractionResponse)
async def extract_policy(file_id: str):
    """
    Extract policy data from uploaded PDF.
    
    Args:
        file_id: Unique identifier of uploaded file
        
    Returns:
        ExtractionResponse with extracted policy data
    """
    # Check if file exists
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    
    try:
        # Step 1: Extract text using OCR
        extracted_text = await extract_text_from_pdf(file_path)
        
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF"
            )
        
        # Step 2: Use AI to extract structured data
        policy_data = await extract_policy_data(extracted_text)
        
        return ExtractionResponse(
            success=True,
            message="Policy data extracted successfully",
            data=policy_data,
            extraction_id=file_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {str(e)}"
        )
