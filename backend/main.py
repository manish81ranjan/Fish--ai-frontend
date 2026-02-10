import os
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    render_template,
    session,
    redirect
)
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

from backend.config import Config
from backend.extensions import bcrypt, jwt

# ---------- BLUEPRINTS ----------
from backend.routes.auth import auth_bp
from backend.routes.products import products_bp
from backend.routes.cart import cart_bp
from backend.routes.orders import orders_bp
from backend.routes.ai import ai_bp
from backend.routes.accessories import api_accessories, accessories_site


# ================== APP FACTORY ==================
def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
    FRONTEND_PAGES = os.path.join(FRONTEND_DIR, "pages")
    FRONTEND_JS = os.path.join(FRONTEND_DIR, "js")
    FRONTEND_CSS = os.path.join(FRONTEND_DIR, "css")

    app = Flask(
        __name__,
        template_folder=FRONTEND_PAGES,
        static_folder=os.path.join(BASE_DIR, "static"),
        static_url_path="/static",
    )

    # ---------- CONFIG ----------
    app.config.from_object(Config)
    app.secret_key = app.config["SECRET_KEY"]

    # ---------- CORS ----------
    CORS(app, supports_credentials=True)

    # ---------- MONGODB ----------
    mongo = PyMongo(app)
    app.mongo = mongo  # available as current_app.mongo

    # ---------- EXTENSIONS ----------
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ---------- REGISTER BLUEPRINTS ----------
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(api_accessories)
    app.register_blueprint(accessories_site)

    # ---------- API HEALTH CHECK ----------
    @app.route("/api")
    def api_test():
        return jsonify({"message": "Backend running 🚀"})

    # ---------- FRONTEND ROUTES ----------
    @app.route("/")
    def home():
        return send_from_directory(FRONTEND_PAGES, "index.html")

    @app.route("/js/<path:file>")
    def serve_js(file):
        return send_from_directory(FRONTEND_JS, file)

    @app.route("/css/<path:file>")
    def serve_css(file):
        return send_from_directory(FRONTEND_CSS, file)

    @app.route("/<path:page>")
    def serve_pages(page):
        if page.startswith("api"):
            return jsonify({"error": "Invalid API route"}), 404
        return send_from_directory(FRONTEND_PAGES, page)

    # ---------- SITE PAGES ----------
    @app.route("/marketplace")
    def marketplace():
        products = list(app.mongo.db.products.find())
        return render_template("marketplace.html", fishes=products)

    @app.route("/ai-fish")
    def ai_fish():
        return render_template("ai-fish.html")

    @app.route("/cart")
    def cart():
        return render_template("cart.html")

    @app.route("/orders")
    def orders():
        return render_template("orders.html")

    @app.route("/auth")
    def auth():
        if "user_id" in session:
            return redirect("/profile")
        return render_template("auth.html")

    @app.route("/profile")
    def profile():
        return render_template("profile.html")

    @app.route("/checkout")
    def checkout():
        return render_template("checkout.html")

    @app.route("/product/<pid>")
    def product_page(pid):
        product = None

        if ObjectId.is_valid(pid):
            product = app.mongo.db.products.find_one({"_id": ObjectId(pid)})

        if not product:
            product = app.mongo.db.products.find_one({"id": int(pid)}) if pid.isdigit() else None

        if not product:
            return "Product not found", 404

        return render_template("product.html", p=product)

    @app.route("/accessories")
    def accessories():
        accessories = list(app.mongo.db.accessories.find())
        return render_template("accessories.html", accessories=accessories)

    return app


# ================== RENDER ENTRYPOINT ==================
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
