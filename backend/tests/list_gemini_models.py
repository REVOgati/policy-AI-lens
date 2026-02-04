"""
List available Gemini models
"""
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)

print("Available Gemini Models:")
print("=" * 60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Methods: {model.supported_generation_methods}")
            print()
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying common model names...")

    common_models = [
        'gemini-pro',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'models/gemini-pro',
        'models/gemini-1.5-pro',
    ]

    for model_name in common_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'OK'")
            print(f"✅ {model_name} - WORKS")
        except Exception as e:
            print(f"❌ {model_name} - {str(e)[:50]}")
