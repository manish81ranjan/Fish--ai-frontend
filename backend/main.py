# import os
# from flask import (
#     Flask,
#     jsonify,
#     send_from_directory,
#     render_template,
#     session,
#     redirect
# )
# from flask_cors import CORS
# from flask_pymongo import PyMongo
# from bson import ObjectId

# from backend.config import Config
# from backend.extensions import mongo, bcrypt, jwt


# # ---------- BLUEPRINTS ----------
# from backend.routes.auth import auth_bp
# from backend.routes.products import products_bp
# from backend.routes.cart import cart_bp
# from backend.routes.orders import orders_bp
# from backend.routes.ai import ai_bp
# from backend.routes.accessories import api_accessories, accessories_site


# # ================== APP FACTORY ==================
# def create_app():
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#     FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
#     FRONTEND_PAGES = os.path.join(FRONTEND_DIR, "pages")
#     FRONTEND_JS = os.path.join(FRONTEND_DIR, "js")
#     FRONTEND_CSS = os.path.join(FRONTEND_DIR, "css")

#     app = Flask(
#         __name__,
#         template_folder=FRONTEND_PAGES,
#         static_folder=os.path.join(BASE_DIR, "static"),
#         static_url_path="/static",
#     )

#     # ---------- CONFIG ----------
#     app.config.from_object(Config)
#     app.secret_key = app.config["SECRET_KEY"]

#     if not app.config.get("MONGO_URI"):
#         raise RuntimeError("❌ MONGO_URI not set")

#     # ---------- CORS ----------
#     CORS(app, supports_credentials=True)

#     # ---------- EXTENSIONS ----------
#     mongo.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)

#     # ---------- BLUEPRINTS ----------
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(products_bp)
#     app.register_blueprint(cart_bp)
#     app.register_blueprint(orders_bp)
#     app.register_blueprint(ai_bp)
#     app.register_blueprint(api_accessories)
#     app.register_blueprint(accessories_site)

#     # ---------- HEALTH ----------
#     @app.route("/api")
#     def api_test():
#         return jsonify({"message": "Backend running 🚀"})

#     # ---------- FRONTEND ----------
#     @app.route("/")
#     def home():
#         return send_from_directory(FRONTEND_PAGES, "index.html")

#     @app.route("/js/<path:file>")
#     def serve_js(file):
#         return send_from_directory(FRONTEND_JS, file)

#     @app.route("/css/<path:file>")
#     def serve_css(file):
#         return send_from_directory(FRONTEND_CSS, file)

#     @app.route("/<path:page>")
#     def serve_pages(page):
#         if page.startswith("api"):
#             return jsonify({"error": "Invalid API route"}), 404
#         return send_from_directory(FRONTEND_PAGES, page)

#     return app



# # ================== RENDER ENTRYPOINT ==================
# app = create_app()

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)



import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from backend.config import Config
from backend.extensions import mongo, bcrypt, jwt

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

    # Frontend paths
    FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))
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

    if not app.config.get("MONGO_URI"):
        raise RuntimeError("❌ MONGO_URI not set")

    # ---------- CORS ----------
    CORS(
        app,
        supports_credentials=True,
        resources={r"/api/*": {"origins": "*"}}
    )

    # ---------- EXTENSIONS ----------
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ---------- BLUEPRINTS ----------
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(api_accessories)
    app.register_blueprint(accessories_site)

    # ---------- HEALTH CHECK ----------
    @app.route("/api")
    def api_test():
        return jsonify({"status": "ok", "message": "Backend running 🚀"})

    # ---------- FRONTEND ROUTES ----------
    @app.route("/")
    def home():
        return send_from_directory(FRONTEND_PAGES, "index.html")

    @app.route("/js/<path:filename>")
    def serve_js(filename):
        return send_from_directory(FRONTEND_JS, filename)

    @app.route("/css/<path:filename>")
    def serve_css(filename):
        return send_from_directory(FRONTEND_CSS, filename)

    @app.route("/<path:page>")
    def serve_pages(page):
        if page.startswith("api"):
            return jsonify({"error": "Invalid API route"}), 404
        return send_from_directory(FRONTEND_PAGES, page)

    return app


# ================== APP INSTANCE (Render) ==================
app = create_app()


# ================== LOCAL RUN ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

