# from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from main import db
# from backend.models import review
from extensions import db
from models.product import Product
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os
from models.review import Review
from flask import Blueprint, request, jsonify, render_template, redirect, url_for


products_bp = Blueprint("products", __name__, url_prefix="/api/products")

@products_bp.route("/", methods=["POST"])
@jwt_required()
def add_product():
    data = request.get_json()
    user_id = get_jwt_identity()

    product = Product(
        name=data.get("name"),
        price=data.get("price"),
        stock=data.get("stock"),
        description=data.get("description"),
        category=data.get("category"),
        seller_id=user_id
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Fish added successfully"}), 201


@products_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()

    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock,
            "description": p.description,
            "category": p.category
        })

    return jsonify(result), 200


@products_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "description": product.description,
        "category": product.category
    })


@products_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    user_id = get_jwt_identity()

    if product.seller_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    product.description = data.get("description", product.description)
    product.category = data.get("category", product.category)

    db.session.commit()

    return jsonify({"message": "Fish updated"}), 200


@products_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    user_id = get_jwt_identity()

    if product.seller_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Fish deleted"}), 200

from flask import Blueprint, render_template
from models.product import Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/marketplace")
def marketplace():
    products = Product.query.all()
    return render_template("marketplace.html", products=products)


from models.review import Review
from models.product import Product

@products_bp.route("/product/<int:id>")
def product_page(id):
    product = Product.query.get_or_404(id)

    reviews = Review.query.filter_by(product_id=id).order_by(Review.id.desc()).all()

    related = Product.query.filter(Product.category==product.category, Product.id!=id).limit(12).all()

    return render_template("product.html", p=product, reviews=reviews, related=related)




import uuid

UPLOAD_REVIEW_IMAGES = "static/reviews"
UPLOAD_REVIEW_VIDEOS = "static/review_videos"
os.makedirs(UPLOAD_REVIEW_IMAGES, exist_ok=True)
os.makedirs(UPLOAD_REVIEW_VIDEOS, exist_ok=True)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "reviews")
VIDEO_DIR = os.path.join(BASE_DIR, "static", "review_videos")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


@products_bp.route("/add-review", methods=["POST"])
def add_review():

    product_id = request.form.get("product_id")
    name = request.form.get("name")
    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if not all([product_id, name, rating, comment]):
        return jsonify({"error": "Missing required fields"}), 400

    image_files = request.files.getlist("images")
    video_file = request.files.get("video")

    image_names = []
    for img in image_files:
        if img.filename:
            ext = img.filename.split(".")[-1]
            fname = f"{uuid.uuid4()}.{ext}"
            img.save(os.path.join(IMAGE_DIR, fname))
            image_names.append(fname)

    video_name = None
    if video_file and video_file.filename:
        vext = video_file.filename.split(".")[-1]
        video_name = f"{uuid.uuid4()}.{vext}"
        video_file.save(os.path.join(VIDEO_DIR, video_name))

    review = Review(
        product_id=product_id,
        name=name,
        rating=rating,
        comment=comment,
        images=",".join(image_names),
        video=video_name,
        likes=0
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review added successfully"}), 201






