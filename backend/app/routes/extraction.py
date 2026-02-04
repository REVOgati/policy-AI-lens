"""
Extraction route - handles direct AI extraction from PDF using Gemini Vision.
"""
import os

from fastapi import APIRouter, HTTPException

from app.models.schemas import ExtractionResponse
from app.services.ai_service import extract_policy_data_from_file
from app.services.ocr_service import extract_text_from_pdf  # For debug endpoint
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/extract/{file_id}", response_model=ExtractionResponse)
async def extract_policy(file_id: str):
    """
    Extract policy data directly from uploaded PDF using Gemini Vision.

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
        print(
            f"\n🚀 Starting direct Gemini Vision extraction for file: {file_id}")
        print("=" * 70)

        # Extract policy data directly from PDF using Gemini Vision
        policy_data = await extract_policy_data_from_file(file_path)

        print("=" * 70)
        print("✅ Extraction complete!")
        print("=" * 70 + "\n")

        return ExtractionResponse(
            success=True,
            message="Policy data extracted successfully using Gemini Vision",
            data=policy_data,
            extraction_id=file_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {str(e)}"
        ) from e


@router.get("/debug/ocr/{file_id}")
async def debug_ocr_text(file_id: str):
    """
    Debug endpoint: View raw OCR extracted text without AI processing.

    Args:
        file_id: Unique identifier of uploaded file

    Returns:
        Raw extracted text from OCR
    """
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    try:
        # Extract text using OCR
        extracted_text = await extract_text_from_pdf(file_path)

        return {
            "success": True,
            "file_id": file_id,
            "text_length": len(extracted_text),
            "raw_text": extracted_text,
            "preview": extracted_text[:1000]  # First 1000 chars preview
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR extraction failed: {str(e)}"
        ) from e
