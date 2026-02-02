"""
Configuration settings for the Policy AI Lens application.
Loads environment variables and provides application settings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
   
    # API Configuration
    gemini_api_key: str
    
    # Application Settings
    app_env: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # File Upload Settings
    max_upload_size: int = 10485760  # 10MB
    allowed_extensions: list = [".pdf"]
    upload_dir: str = "uploads"
    
    # OCR Settings
    tesseract_path: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # Google Sheets Configuration (for Phase 3)
    google_sheets_credentials_file: str = ""
    google_sheet_id: str = ""
    
    # CORS Settings
    cors_origins: list = [
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React default
    ]
    
    class Config:
        # Load environment variables from envs directory
        env_file = os.path.join("envs", ".env.dev")
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
