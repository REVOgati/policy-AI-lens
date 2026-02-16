"""
Configuration settings for the Policy AI Lens application.
Loads environment variables and provides application settings.
"""
import os
from functools import lru_cache

from pydantic_settings import BaseSettings


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
    google_sheet_name: str = "Database_One"  # Name of the worksheet within the spreadsheet

    # CORS Settings
    cors_origins: list = [
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React default
    ]

    class Config:
        # Load environment file based on APP_ENV (defaults to 'dev' for development)
        # Use 'dev' or 'prod' as the suffix
        app_env = os.getenv("APP_ENV", "dev")
        env_file = os.path.join("envs", f".env.{app_env}")
        env_file_encoding = 'utf-8'
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
