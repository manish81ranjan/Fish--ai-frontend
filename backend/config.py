import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env
load_dotenv()


class Config:
    # ================== CORE ==================
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

    # ================== ENV ==================
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"

    # ================== DATABASE ==================
    MONGO_URI = os.getenv("MONGO_URI")

    if not MONGO_URI:
        raise RuntimeError("❌ MONGO_URI is not set")

    # ================== JWT ==================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 86400))
    )

    # ================== FILE UPLOAD ==================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "static/uploads")
    )

    MAX_CONTENT_LENGTH = int(
        os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)
    )

    # ================== CORS ==================
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
