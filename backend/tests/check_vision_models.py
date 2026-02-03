"""
Check available Gemini models and their vision capabilities
"""
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)

print("="*70)
print("Available Gemini Models:")
print("="*70)

for model in genai.list_models():
    # Check if model supports generateContent
    if 'generateContent' in model.supported_generation_methods:
        print(f"\n✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print(f"   Input Types: {model.supported_generation_methods}")
        
        # Check if it supports vision (has image input)
        if hasattr(model, 'input_token_limit'):
            print(f"   Input Token Limit: {model.input_token_limit}")

print("\n" + "="*70)
