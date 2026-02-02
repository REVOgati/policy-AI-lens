"""
Upload route - handles PDF file uploads.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing.
    
    Args:
        file: PDF file to upload
        
    Returns:
        JSON response with file_id and filename
    """
    # Validate file extension
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Check file size
    contents = await file.read()
    if len(contents) > settings.max_upload_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.max_upload_size} bytes"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Ensure upload directory exists
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "File uploaded successfully",
            "file_id": file_id,
            "filename": file.filename
        }
    )
