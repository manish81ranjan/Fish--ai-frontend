# import os
# from urllib.parse import quote_plus

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

#     RAW_MONGO_USER = os.getenv("MONGO_USER")
#     RAW_MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
#     MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
#     MONGO_DB = os.getenv("MONGO_DB")

#     # ---- SAFETY CHECK ----
#     if not all([RAW_MONGO_USER, RAW_MONGO_PASSWORD, MONGO_CLUSTER, MONGO_DB]):
#         raise RuntimeError("❌ MongoDB environment variables are missing")

#     MONGO_USER = quote_plus(RAW_MONGO_USER)
#     MONGO_PASSWORD = quote_plus(RAW_MONGO_PASSWORD)

#     MONGO_URI = (
#         f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
#         f"@{MONGO_CLUSTER}/{MONGO_DB}"
#         f"?retryWrites=true&w=majority"
#     )

# import os
# from urllib.parse import quote_plus

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

#     MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
#     MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
#     MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
#     MONGO_DB = os.getenv("MONGO_DB")

#     MONGO_URI = (
#         f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
#         f"@{MONGO_CLUSTER}/{MONGO_DB}"
#         f"?retryWrites=true&w=majority"
#     )

#     JWT_SECRET_KEY = SECRET_KEY

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # ✅ USE DIRECT MONGO URI (RENDER SAFE)
    MONGO_URI = os.getenv("MONGO_URI")

    if not MONGO_URI:
        raise RuntimeError("❌ MONGO_URI is not set")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
