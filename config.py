import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base Configuration Class for EduSmart AI.

    Centralizes all application settings so they can be securely
    managed and easily modified without touching business logic.
    """

    # Secret key used by Flask to sign session cookies securely
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-edusmart-ai-2026")

    # Database URI: Support PostgreSQL (auto-fixing postgres:// to postgresql:// for Render) and SQLite default
    _raw_db_url = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'edusmart.db'}"
    )
    if _raw_db_url and _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _raw_db_url

    # Disable modification tracking overhead to improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads directory configuration (PDF notes, study materials)
    UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads")
    ALLOWED_EXTENSIONS = {"pdf"}

    # Maximum file size: 10 Megabytes (10 * 1024 * 1024 bytes)
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))

    # Google Gemini API Key for AI features (Study Assistant & Quiz Generator)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


class DevelopmentConfig(Config):
    """Configuration used during active local development."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration used when deploying to production."""
    DEBUG = False


class TestingConfig(Config):
    """Configuration used when running automated tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Configuration dictionary for flexible environment switching
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
