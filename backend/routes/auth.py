from flask import Blueprint, request, redirect, render_template, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)
mysql = MySQL()

# ---------- MYSQL INIT ----------
def init_auth(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Man@6jan'
    app.config['MYSQL_DB'] = 'fish_ai_market'
    mysql.init_app(app)

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
    name = request.form["name"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
            (name, email, password)
        )
        mysql.connection.commit()
        flash("Signup successful", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash("Email already exists", "error")
    finally:
        cur.close()

    return redirect("/profile")

@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, password FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[2], password):
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        return redirect("/")

    flash("Invalid email or password", "error")
    return redirect("/profile")

@auth_bp.route("/auth")
def auth():
    if "user_id" not in session:
        return redirect("/profile")

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT name, email FROM users WHERE id=%s",
        (session["user_id"],)
    )
    user = cur.fetchone()
    cur.close()

    if not user:
        session.clear()
        return redirect("/profile")

    return render_template("auth.html", name=user[0], email=user[1])
