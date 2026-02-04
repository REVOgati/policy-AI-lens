"""
OCR Service - Extracts text from PDF files using PyMuPDF and Tesseract.
"""
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from app.config import get_settings
from PIL import Image
import os

settings = get_settings()

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path


async def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF first, fallback to Tesseract OCR.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text as string
    """
    extracted_text = ""

    try:
        # Method 1: Try PyMuPDF for native text extraction
        doc = fitz.open(file_path)
        for page in doc:
            text = page.get_text()
            if text.strip():
                extracted_text += text + "\n"
        doc.close()

        # If we got any text, return it (lowered threshold for testing)
        if len(extracted_text.strip()) > 10000:
            print(
                f"✅ Extracted {len(extracted_text)} characters using PyMuPDF")
            return extracted_text
        else:
            print(
                f"⚠️  PyMuPDF extracted only {len(extracted_text)} characters, trying OCR...")

    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")

    # Method 2: Fallback to Tesseract OCR for scanned PDFs
    try:
        print("Falling back to Tesseract OCR...")

        # Search for poppler installation
        poppler_path = None
        base_paths = [
            # Manual install (specific version)
            r"C:\Program Files\poppler\poppler-24.08.0\Library\bin",
            r"C:\Program Files\poppler",  # Manual install (any version)
            os.path.join(os.getcwd(), "poppler"),  # Local project directory
            r"C:\ProgramData\chocolatey\lib\poppler\tools",  # Chocolatey
        ]

        for base in base_paths:
            if os.path.exists(base):
                # If it's already a bin directory with pdftoppm.exe, use it
                # directly
                if os.path.exists(os.path.join(base, 'pdftoppm.exe')):
                    poppler_path = base
                    print(f"✅ Found poppler at: {poppler_path}")
                    break
                # Otherwise, search recursively
                for root, dirs, files in os.walk(base):
                    if 'pdftoppm.exe' in files:
                        poppler_path = root
                        print(f"✅ Found poppler at: {poppler_path}")
                        break
                if poppler_path:
                    break

        if poppler_path:
            images = convert_from_path(
                file_path, dpi=300, poppler_path=poppler_path)
        else:
            print("⚠️  Poppler not found, trying system PATH...")
            images = convert_from_path(file_path, dpi=300)

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='eng')
            extracted_text += text + "\n"
            print(f"Processed page {i+1}/{len(images)}")

        print(
            f"Extracted {len(extracted_text)} characters using Tesseract OCR")
        return extracted_text

    except Exception as e:
        raise Exception(f"OCR extraction failed: {str(e)}")
