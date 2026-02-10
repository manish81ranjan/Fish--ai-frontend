from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    session,
    flash,
    current_app
)
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

auth_bp = Blueprint("auth", __name__)


# ===================== ROUTES =====================

@auth_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect("/profile")
    return render_template("index.html")


@auth_bp.route("/profile")
def profile_page():
    session.clear()
    return render_template("profile.html")


# ===================== SIGNUP =====================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        flash("All fields are required", "error")
        return redirect("/profile")

    mongo = current_app.mongo
    users = mongo.db.users

    # Check if email already exists
    if users.find_one({"email": email}):
        flash("Email already exists", "error")
        return redirect("/profile")

    hashed_password = generate_password_hash(password)

    users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    flash("Signup successful", "success")
    return redirect("/profile")


# ===================== LOGIN =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    mongo = current_app.mongo
    user = mongo.db.users.find_one({"email": email})

    if user and check_password_hash(user["password"], password):
        session["user_id"] = str(user["_id"])
        session["user_name"] = user["name"]
        return redirect("/")

    flash("Invalid email or password", "error")
    return redirect("/profile")


# ===================== AUTH PAGE =====================
@auth_bp.route("/auth")
def auth():
    if "user_id" not in session:
        return redirect("/profile")

    mongo = current_app.mongo

    try:
        user = mongo.db.users.find_one(
            {"_id": ObjectId(session["user_id"])}
        )
    except Exception:
        session.clear()
        return redirect("/profile")

    if not user:
        session.clear()
        return redirect("/profile")

    return render_template(
        "auth.html",
        name=user["name"],
        email=user["email"]
    )
