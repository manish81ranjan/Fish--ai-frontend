import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # =========================
    # DATABASE (MongoDB)
    # =========================
    # Example:
    # mongodb+srv://user:pass@cluster.mongodb.net/fish_ai_market
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/fish_ai_market"
    )

    # =========================
    # FILE UPLOADS
    # =========================
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "uploads", "fish_images")
    )

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit
