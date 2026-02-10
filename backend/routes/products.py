import os
import uuid
from bson import ObjectId
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from backend.extensions import mongo  # ✅ FIXED IMPORT


# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGE_DIR = os.path.join(BASE_DIR, "static", "reviews")
VIDEO_DIR = os.path.join(BASE_DIR, "static", "review_videos")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


# =========================
# BLUEPRINT
# =========================
products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/api/products"
)


# =========================
# PRODUCTS API
# =========================
@products_bp.route("/", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()
    user_id = get_jwt_identity()

    product = {
        "name": data.get("name"),
        "price": int(data.get("price")),
        "stock": int(data.get("stock")),
        "description": data.get("description"),
        "category": data.get("category"),
        "seller_id": ObjectId(user_id)
    }

    mongo.db.products.insert_one(product)

    return jsonify({"message": "Product added successfully"}), 201


@products_bp.route("/", methods=["GET"])
def get_products():
    products = mongo.db.products.find()
    result = []

    for p in products:
        result.append({
            "id": str(p["_id"]),
            "name": p["name"],
            "price": p["price"],
            "stock": p["stock"],
            "description": p.get("description"),
            "category": p.get("category")
        })

    return jsonify(result), 200


@products_bp.route("/<id>", methods=["GET"])
def get_product(id):
    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "stock": product["stock"],
        "description": product.get("description"),
        "category": product.get("category")
    })


@products_bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    user_id = get_jwt_identity()
    product = mongo.db.products.find_one({"_id": ObjectId(id)})

    if not product:
        return jsonify({"message": "Product not found"}), 404

    if str(product["seller_id"]) != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    mongo.db.products.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "name": data.get("name", product["name"]),
            "price": int(data.get("price", product["price"])),
            "stock": int(data.get("stock", product["stock"])),
            "description": data.get("description", product.get("description")),
            "category": data.get("category", product.get("category"))
        }}
    )

    return jsonify({"message": "Product updated"}), 200


@products_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    user_id = get_jwt_identity()
    product = mongo.db.products.find_one({"_id": ObjectId(id)})

    if not product:
        return jsonify({"message": "Product not found"}), 404

    if str(product["seller_id"]) != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    mongo.db.products.delete_one({"_id": ObjectId(id)})

    return jsonify({"message": "Product deleted"}), 200


# =========================
# MARKETPLACE PAGES
# =========================
@products_bp.route("/marketplace", methods=["GET"])
def marketplace():
    products = list(mongo.db.products.find())
    return render_template("marketplace.html", products=products)


@products_bp.route("/product/<id>", methods=["GET"])
def product_page(id):
    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return "Product not found", 404

    reviews = list(
        mongo.db.reviews.find({"product_id": ObjectId(id)})
        .sort("_id", -1)
    )

    related = list(
        mongo.db.products.find({
            "category": product.get("category"),
            "_id": {"$ne": product["_id"]}
        }).limit(12)
    )

    return render_template(
        "product.html",
        p=product,
        reviews=reviews,
        related=related
    )


# =========================
# ADD REVIEW
# =========================
@products_bp.route("/add-review", methods=["POST"])
def add_review():
    product_id = request.form.get("product_id")
    name = request.form.get("name")
    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if not all([product_id, name, rating, comment]):
        return jsonify({"message": "Missing required fields"}), 400

    images = request.files.getlist("images")
    video = request.files.get("video")

    image_names = []
    for img in images:
        if img.filename:
            ext = img.filename.rsplit(".", 1)[-1]
            fname = f"{uuid.uuid4()}.{ext}"
            img.save(os.path.join(IMAGE_DIR, fname))
            image_names.append(fname)

    video_name = None
    if video and video.filename:
        vext = video.filename.rsplit(".", 1)[-1]
        video_name = f"{uuid.uuid4()}.{vext}"
        video.save(os.path.join(VIDEO_DIR, video_name))

    review = {
        "product_id": ObjectId(product_id),
        "name": name,
        "rating": int(rating),
        "comment": comment,
        "images": image_names,
        "video": video_name,
        "likes": 0
    }

    mongo.db.reviews.insert_one(review)

    return jsonify({"message": "Review added successfully"}), 201
