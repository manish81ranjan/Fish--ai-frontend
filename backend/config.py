import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # =========================
    # DATABASE (Railway MySQL)
    # =========================
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqldb://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # FILE UPLOADS
    # =========================
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "uploads/fish_images")
    )
