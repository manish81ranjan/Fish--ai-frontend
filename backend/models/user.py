from bson import ObjectId
from datetime import datetime
from backend.extensions import mongo


# =========================
# CREATE USER
# =========================
def create_user(name, email, password):
    """
    Creates a new user document in MongoDB
    """
    return mongo.db.users.insert_one({
        "name": name,
        "email": email,
        "password": password,   # already hashed
        "created_at": datetime.utcnow()
    })


# =========================
# GET USER BY EMAIL
# =========================
def get_user_by_email(email):
    """
    Fetch user using email
    """
    return mongo.db.users.find_one({"email": email})


# =========================
# GET USER BY ID
# =========================
def get_user_by_id(user_id):
    """
    Fetch user using ObjectId
    """
    try:
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


# =========================
# SERIALIZE USER (SAFE)
# =========================
def serialize_user(user):
    """
    Convert Mongo user document to JSON-safe dict
    (Never expose password)
    """
    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "created_at": user.get("created_at")
    }
