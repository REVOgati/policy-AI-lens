"""
AI Service - Uses Google Gemini Vision to extract structured policy data directly from PDF.
"""
import google.generativeai as genai
from app.config import get_settings
from app.models.schemas import PolicyData
import json
from PIL import Image
import fitz  # PyMuPDF
import io

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
- sum_insured: Look for: "SUM INSURED", "Sum Insured", "Coverage Amount", "Limit of Liability" (if shown as "-" or blank, use null)
- commencing_date: Look for: "COMMENCING DATE", "Commencement Date", "Start Date", "Effective From", "Period From" (keep original format: DD/MM/YYYY or DD.MM.YYYY)
- expiring_date: Look for: "EXPIRING DATE", "Expiry Date", "Expiration Date", "Valid Until", "Period To" (keep original format: DD/MM/YYYY or DD.MM.YYYY)
- premium_amount: Look for: "PREMIUM", "Premium Amount", "Total Premium", any monetary value associated with premium
- policy_type: Look for: "Motor Third Party", "Comprehensive", "Third Party Fire & Theft", "Life", "Health" (type of insurance coverage)

SPECIAL INSTRUCTIONS:
- Carefully read ALL text in the document, including headers, tables, and fine print
- For Motor Third Party policies, sum_insured is often N/A (use null)
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
            
            # Render page to image at high resolution (300 DPI)
            mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
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
            'models/gemini-2.5-flash',         # Stable multimodal (you've used this successfully)
            'models/gemini-flash-latest',      # Latest Flash (good quota usually)
            'models/gemini-2.0-flash',         # Gemini 2.0 Flash
            'models/gemini-3-flash-preview',   # Gemini 3 Flash (faster, less quota usage)
            'models/gemini-2.5-pro',           # More capable but uses more quota
            'models/gemini-3-pro-preview',     # Gemini 3 Pro (quota exhausted currently)
        ]
        
        model = None
        last_error = None
        last_error = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
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
        response = model.generate_content(content)
        
        # Parse JSON from response
        response_text = response.text.strip()
        
        print("\n" + "="*70)
        print("AI RESPONSE:")
        print("="*70)
        print(response_text[:500])
        print("="*70 + "\n")
        
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
        
        return policy_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return empty policy data if parsing fails
        return PolicyData()
        
    except Exception as e:
        print(f"❌ AI extraction error: {e}")
        raise Exception(f"AI extraction failed: {str(e)}")
