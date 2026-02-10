from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from bson import ObjectId

from backend.extensions import mongo  # ✅ FIXED IMPORT


# =========================
# BLUEPRINT
# =========================
users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users"
)


# =========================
# REGISTER USER
# =========================
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 409

    user = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password)
    }

    mongo.db.users.insert_one(user)

    return jsonify({"message": "User registered successfully"}), 201


# =========================
# LOGIN USER
# =========================
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]))

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200


# =========================
# GET CURRENT USER
# =========================
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()

    user = mongo.db.users.find_one(
        {"_id": ObjectId(user_id)},
        {"password": 0}
    )

    if not user:
        return jsonify({"message": "User not found"}), 404

    user["_id"] = str(user["_id"])

    return jsonify(user), 200


# =========================
# UPDATE USER PROFILE
# =========================
@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    data = request.get_json()

    update_data = {}

    if "name" in data:
        update_data["name"] = data["name"]

    if "password" in data:
        update_data["password"] = generate_password_hash(data["password"])

    if not update_data:
        return jsonify({"message": "Nothing to update"}), 400

    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    return jsonify({"message": "Profile updated"}), 200

