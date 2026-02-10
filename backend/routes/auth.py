# from flask import (
#     Blueprint,
#     request,
#     redirect,
#     render_template,
#     session,
#     flash,
#     current_app
# )
# from flask_bcrypt import Bcrypt
# from bson.objectid import ObjectId

# auth_bp = Blueprint("auth", __name__)
# bcrypt = Bcrypt()


# # ===================== HOME =====================
# @auth_bp.route("/")
# def index():
#     if "user_id" not in session:
#         return redirect("/profile")
#     return render_template("index.html")


# # ===================== PROFILE / LOGIN PAGE =====================
# @auth_bp.route("/profile")
# def profile_page():
#     return render_template("profile.html")


# # ===================== SIGNUP =====================
# @auth_bp.route("/signup", methods=["POST"])
# def signup():
#     name = request.form.get("name")
#     email = request.form.get("email")
#     password = request.form.get("password")

#     if not name or not email or not password:
#         flash("All fields are required", "error")
#         return redirect("/profile")

#     mongo = current_app.mongo
#     users = mongo.db.users

#     if users.find_one({"email": email}):
#         flash("Email already exists", "error")
#         return redirect("/profile")

#     hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

#     users.insert_one({
#         "name": name,
#         "email": email,
#         "password": hashed_password
#     })

#     flash("Signup successful. Please login.", "success")
#     return redirect("/profile")


# # ===================== LOGIN =====================
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     email = request.form.get("email")
#     password = request.form.get("password")

#     mongo = current_app.mongo
#     user = mongo.db.users.find_one({"email": email})

#     if user and bcrypt.check_password_hash(user["password"], password):
#         session["user_id"] = str(user["_id"])
#         session["user_name"] = user["name"]
#         return redirect("/auth")

#     flash("Invalid email or password", "error")
#     return redirect("/profile")


# # ===================== AUTH DASHBOARD =====================
# @auth_bp.route("/auth")
# def auth_dashboard():
#     if "user_id" not in session:
#         return redirect("/profile")

#     mongo = current_app.mongo

#     try:
#         user = mongo.db.users.find_one({
#             "_id": ObjectId(session["user_id"])
#         })
#     except Exception:
#         session.clear()
#         return redirect("/profile")

#     if not user:
#         session.clear()
#         return redirect("/profile")

#     return render_template(
#         "auth.html",
#         name=user.get("name"),
#         email=user.get("email")
#     )


# # ===================== LOGOUT =====================
# @auth_bp.route("/logout")
# def logout():
#     session.clear()
#     flash("Logged out successfully", "success")
#     return redirect("/profile")

from flask import Blueprint, request, jsonify
from backend.extensions import mongo, bcrypt
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    users = mongo.db.users

    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    users.insert_one({
        "email": data["email"],
        "password": hashed_pw
    })

    return jsonify({"message": "Signup successful"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    users = mongo.db.users

    user = users.find_one({"email": data["email"]})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200

