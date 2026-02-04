"""
AI Service - Uses Google Gemini Vision to extract structured policy data directly from PDF.
"""
import io
import json

import fitz  # PyMuPDF
import google.generativeai as genai
from PIL import Image

from app.config import get_settings
from app.models.schemas import PolicyData

settings = get_settings()

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


async def extract_policy_data_from_file(file_path: str) -> PolicyData:
    """
    Extract structured policy data directly from PDF using Gemini Vision.

    Args:
        file_path: Path to the PDF file

    Returns:
        PolicyData object with extracted fields
    """
    # Create the prompt for structured extraction
    prompt = """
You are an expert insurance document analyzer specializing in Kenyan insurance certificates. Carefully examine this insurance policy document image and extract the following information.

Return ONLY a valid JSON object with these exact fields (use null for missing values):

- policy_holder: Look for: "POLICY HOLDER", "Policy Holder", "Insured", "Owner", "Client Name", or the person/entity owning the policy. NOTE: Many motor certificates don't include this - use null if not found.
- policy_number: Look for: "Policy Number", "Ref number", "Policy No", "Certificate No", or unique policy identifier (format: letters/numbers with slashes)
- insurer_name: Look for: "ISSUED BY", "Issuing Office", "Insurance Company", "Insurer" (the company providing insurance)
- sum_insured: For COMPREHENSIVE policies ONLY, look for: "SUM INSURED", "Coverage Amount", "Limit of Liability". For Third Party or non-comprehensive, use "-" to indicate N/A
- commencing_date: Look for: "COMMENCING DATE", "Commencement Date", "Start Date", "Effective From", "Period From" (keep original format: DD/MM/YYYY or DD.MM.YYYY)
- expiring_date: Look for: "EXPIRING DATE", "Expiry Date", "Expiration Date", "Valid Until", "Period To" (keep original format: DD/MM/YYYY or DD.MM.YYYY)
- premium_amount: Look for: "PREMIUM", "Premium Amount", "Total Premium", any monetary value associated with premium
- paid_amount: Look for: "PAID", "Amount Paid", "Payment", "Paid Amount" (typically null, user will enter manually)
- balance_amount: Look for: "BALANCE", "Balance Due", "Amount Due", "Outstanding" (typically null, user will enter manually)
- policy_type: Look for: "Motor Third Party", "Comprehensive", "Third Party Fire & Theft", "Life", "Health" (type of insurance coverage)

SPECIAL INSTRUCTIONS:
- Carefully read ALL text in the document, including headers, tables, and fine print
- For Motor Third Party and non-Comprehensive policies, sum_insured should be "-" (not applicable)
- For Comprehensive policies only, extract the actual sum_insured value
- Keep dates in their ORIGINAL format (DD/MM/YYYY or DD.MM.YYYY) - DO NOT convert format
- If you see "Date: 17.11.2025" near digital signature, it's the certificate issue date, NOT a policy date
- Many motor certificates don't include policy holder name, commencing date, or expiring date - this is normal
- Look carefully at the document structure - some fields may be implied or abbreviated
- Pay attention to table layouts and field labels
- Return ONLY the JSON object, no additional text or explanation
- Use exact field names as specified above

JSON Output:
"""

    try:
        print(f"📄 Converting PDF to images: {file_path}")

        # Open PDF and convert to images
        pdf_document = fitz.open(file_path)
        images = []

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]

            # Render page to image at good resolution (200 DPI - faster than 300)
            mat = fitz.Matrix(200 / 72, 200 / 72)  # 200 DPI for speed
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)

            print(f"✅ Converted page {page_num + 1}/{len(pdf_document)}")

        pdf_document.close()

        print(f"✅ Total pages converted: {len(images)}")

        # Use Gemini vision model - try available models in order of preference
        # Prioritize models with available quota
        model_names = [
            # Stable multimodal (you've used this successfully)
            'models/gemini-2.5-flash',
            'models/gemini-flash-latest',
            # Latest Flash (good quota usually)
            'models/gemini-2.0-flash',         # Gemini 2.0 Flash
            'models/gemini-3-flash-preview',
            # Gemini 3 Flash (faster, less quota usage)
            'models/gemini-2.5-pro',           # More capable but uses more quota
            'models/gemini-3-pro-preview',
            # Gemini 3 Pro (quota exhausted currently)
        ]

        model = None
        last_error = None
        for model_name in model_names:
            try:
                # Configure for faster responses
                generation_config = genai.types.GenerationConfig(
                    temperature=0.1,  # Low temperature for consistency
                    max_output_tokens=2048,  # Increased for 9 fields
                )
                model = genai.GenerativeModel(
                    model_name,
                    generation_config=generation_config
                )
                print(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                last_error = str(e)
                print(f"⚠️  Model {model_name} not available: {e}")
                continue

        if not model:
            raise Exception("No available Gemini vision model found")

        # Prepare content with all pages
        content = [prompt]
        for i, img in enumerate(images):
            content.append(img)
            print(f"📎 Added page {i + 1} to request")

        # Generate response with the images
        print("🤖 Generating content from document images...")
        
        # Try with retry logic for transient failures
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = model.generate_content(content)
                break  # Success, exit retry loop
            except Exception as e:
                error_msg = str(e)
                if "504" in error_msg or "Deadline Exceeded" in error_msg:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Timeout on attempt {attempt + 1}, retrying...")
                        continue
                    else:
                        raise Exception(
                            "AI service timeout. The document may be too complex or the service is overloaded. Please try again."
                        )
                elif "429" in error_msg or "quota" in error_msg.lower():
                    raise Exception(
                        "AI service quota exceeded. Please try again in a few minutes."
                    )
                else:
                    raise  # Re-raise other errors

        # Parse JSON from response
        response_text = response.text.strip()

        print("\n" + "=" * 70)
        print("AI RESPONSE (Full):")
        print("=" * 70)
        print(response_text)
        print("=" * 70 + "\n")

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        # Parse JSON
        policy_dict = json.loads(response_text)

        # Create PolicyData object
        policy_data = PolicyData(**policy_dict)
        
        # Post-process: For non-COMP policies, sum_insured should be "-" (not applicable)
        if policy_data.policy_type:
            policy_type_upper = policy_data.policy_type.upper()
            if 'COMP' not in policy_type_upper:
                # Non-comprehensive policies use "-" to represent N/A
                policy_data.sum_insured = "-"
                print("ℹ️  Non-COMP policy detected: sum_insured set to '-' (N/A)")

        return policy_data

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response text length: {len(response_text)} characters")
        print(f"Response text: {response_text}")
        # Return empty policy data if parsing fails
        return PolicyData()

    except Exception as e:
        print(f"❌ AI extraction error: {e}")
        raise Exception(f"AI extraction failed: {str(e)}")
