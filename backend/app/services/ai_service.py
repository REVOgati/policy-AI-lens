"""
AI Service - Uses Google Gemini to extract structured policy data.
"""
import google.generativeai as genai
from app.config import get_settings
from app.models.schemas import PolicyData
import json

settings = get_settings()

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


async def extract_policy_data(text: str) -> PolicyData:
    """
    Extract structured policy data from text using Google Gemini.
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        PolicyData object with extracted fields
    """
    # Create the prompt for structured extraction
    prompt = f"""
You are an expert insurance document analyzer. Extract the following information from the insurance policy document text below.

Return ONLY a valid JSON object with these exact fields (use null for missing values):
- client_name: Name of the policy holder
- policy_number: Unique policy identifier
- insurer_name: Name of the insurance company
- sum_insured: Coverage amount (include currency if present)
- start_date: Policy start date (format: YYYY-MM-DD if possible)
- expiry_date: Policy expiry date (format: YYYY-MM-DD if possible)
- premium_amount: Premium amount (include currency if present)
- policy_type: Type of insurance (e.g., Life, Health, Motor, Home)

IMPORTANT: 
- Return ONLY the JSON object, no additional text
- Use exact field names as specified
- If a field is not found, use null
- Be conservative - only extract if you're confident

Document Text:
{text}

JSON Output:
"""
    
    try:
        # Use Gemini model - try available models in order of preference
        model_names = [
            'models/gemini-2.5-flash',      # Fast, newest version
            'models/gemini-flash-latest',   # Always points to latest flash
            'models/gemini-pro-latest',     # Fallback to pro
            'models/gemini-2.5-pro',        # More capable but slower
        ]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                print(f"⚠️  Model {model_name} not available: {e}")
                continue
        
        if not model:
            raise Exception("No available Gemini model found")
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Parse JSON from response
        response_text = response.text.strip()
        
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
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return empty policy data if parsing fails
        return PolicyData()
        
    except Exception as e:
        print(f"AI extraction error: {e}")
        raise Exception(f"AI extraction failed: {str(e)}")
