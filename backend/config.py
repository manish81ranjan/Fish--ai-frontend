import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
    MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
    MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")  # cluster0.xxxxx.mongodb.net
    MONGO_DB = os.getenv("MONGO_DB", "auronox")

    MONGO_URI = (
        f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
        f"@{MONGO_CLUSTER}/{MONGO_DB}"
        f"?retryWrites=true&w=majority"
    )
