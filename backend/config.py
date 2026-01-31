# import os
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret-key"
    UPLOAD_FOLDER = "uploads/fish_images"
    SECRET_KEY = "fish_secret"
    # SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/fish_ai_market"
    # SQLALCHEMY_DATABASE_URI = "mysql://root:Man@6jan@localhost:3306/fish_ai_market"
    SECRET_KEY = "super-secret-key"

    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:Man%406jan@localhost/fish_ai_market"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
