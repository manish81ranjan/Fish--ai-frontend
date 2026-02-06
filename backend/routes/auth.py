from flask import Blueprint, request, redirect, render_template, session, flash
from backend.extensions import db, bcrypt
from backend.models.user import User

auth_bp = Blueprint("auth", __name__)

# ---------- INIT (kept so your imports don’t break) ----------
def init_auth(app):
    pass


# ---------- ROUTES ----------

@auth_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect("/profile")
    return render_template("index.html")


@auth_bp.route("/profile")
def profile_page():
    session.clear()
    return render_template("profile.html")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        flash("All fields are required", "error")
        return redirect("/profile")

    if User.query.filter_by(email=email).first():
        flash("Email already exists", "error")
        return redirect("/profile")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    flash("Signup successful", "success")
    return redirect("/profile")


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["user_name"] = user.name
        return redirect("/")

    flash("Invalid email or password", "error")
    return redirect("/profile")


@auth_bp.route("/auth")
def auth():
    if "user_id" not in session:
        return redirect("/profile")

    user = User.query.get(session["user_id"])
    if not user:
        session.clear()
        return redirect("/profile")

    return render_template("auth.html", name=user.name, email=user.email)
