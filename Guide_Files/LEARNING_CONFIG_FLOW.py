"""
ENVIRONMENT VARIABLES FLOW - DETAILED EXPLANATION
==================================================

STEP 1: .env.dev file (envs/.env.dev)
----------------------------------------
GEMINI_API_KEY=AIzaSyDD...
TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
MAX_UPLOAD_SIZE=10485760

This is just a TEXT FILE with key=value pairs.


STEP 2: Settings Class (config.py)
----------------------------------------
class Settings(BaseSettings):  # ← Inherits from Pydantic BaseSettings
    # These are FIELD DEFINITIONS (not values yet!)
    gemini_api_key: str  # ← Says "I need a string called gemini_api_key"
    tesseract_path: str
    max_upload_size: int = 10485760  # ← Default value if not in .env
    
    class Config:  # ← This is NESTED class (tells Pydantic HOW to load)
        env_file = os.path.join("envs", ".env.dev")  # ← WHERE to find .env
        case_sensitive = False  # ← GEMINI_API_KEY = gemini_api_key


STEP 3: What Happens When Settings() is Called
------------------------------------------------
When you do: settings = Settings()

Pydantic automatically:
1. Reads envs/.env.dev file
2. Parses each line: GEMINI_API_KEY=AIzaSyDD...
3. Converts to lowercase: gemini_api_key (because case_sensitive=False)
4. Matches to class fields: gemini_api_key: str
5. Validates type (is it a string?)
6. Creates Settings object with actual values

Result: settings.gemini_api_key = "AIzaSyDD..."


STEP 4: get_settings() Function
---------------------------------
@lru_cache()  # ← Caches result (only runs once)
def get_settings() -> Settings:
    return Settings()  # ← Creates Settings object ONCE

First call: Creates Settings, loads .env, returns object
Second call: Returns SAME object (cached, faster)


STEP 5: How Other Files Use It
--------------------------------
# upload.py
from app.config import get_settings  # ← Import the function
settings = get_settings()  # ← Get the cached Settings object

# Now use it:
if len(contents) > settings.max_upload_size:  # ← Access the value!
    raise HTTPException(...)


# ocr_service.py
from app.config import get_settings
settings = get_settings()
pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path  # ← Use it!


VISUAL FLOW DIAGRAM:
====================

envs/.env.dev (TEXT FILE)
    ↓
    ↓ (read by Pydantic when Settings() is instantiated)
    ↓
class Settings(BaseSettings)
    ↓ has nested →  class Config
    ↓                   ↓ env_file = "envs/.env.dev"
    ↓                   ↓ case_sensitive = False
    ↓ ← tells Pydantic "read from this file, ignore case"
    ↓
Settings() object created
    ↓ (contains actual values now)
    ↓ .gemini_api_key = "AIzaSyDD..."
    ↓ .tesseract_path = "C:\\Program Files\\..."
    ↓ .max_upload_size = 10485760
    ↓
get_settings() function
    ↓ (@lru_cache makes it return same object every time)
    ↓
Multiple files import and use:
    ├── upload.py → settings.max_upload_size
    ├── ocr_service.py → settings.tesseract_path
    ├── ai_service.py → settings.gemini_api_key
    └── main.py → settings.host, settings.port


KEY CONCEPTS:
=============

1. NESTED CLASS Config:
   - It's NOT inheriting
   - It's a CONFIGURATION for the parent class
   - Tells Pydantic "here's how to behave"

2. BaseSettings:
   - Special Pydantic class
   - Knows how to read .env files
   - Automatically validates types
   - class Config tells it WHERE and HOW

3. @lru_cache():
   - Python decorator
   - Caches function result
   - First call: runs Settings(), stores result
   - Next calls: returns stored result
   - Why? Loading .env file is slow, do it once!

4. Type Hints:
   - gemini_api_key: str ← must be string
   - max_upload_size: int ← must be integer
   - Pydantic validates when loading


COMMON CONFUSION:
=================
❌ "class Config loads the env variables"
✅ "class Config TELLS Pydantic HOW to load them"

❌ "Settings() reads the file every time"
✅ "get_settings() caches it, Settings() called only once"

❌ "Config class inherits from Settings"
✅ "Config class is NESTED inside Settings (configuration)"


TESTING THE FLOW:
=================
"""

# Run this to see it in action:
from app.config import get_settings

# First call - loads .env file
settings1 = get_settings()
print(f"Gemini API Key: {settings1.gemini_api_key[:20]}...")
print(f"Max Upload: {settings1.max_upload_size}")
print(f"Tesseract: {settings1.tesseract_path}")

# Second call - returns cached object (same instance!)
settings2 = get_settings()
print(f"\nSame object? {settings1 is settings2}")  # True!

# Access any setting
print(f"\nHost: {settings1.host}")
print(f"Port: {settings1.port}")
print(f"Debug: {settings1.debug}")
