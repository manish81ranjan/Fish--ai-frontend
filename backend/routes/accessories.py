import os
import uuid
from bson import ObjectId
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required

from backend.extensions import mongo


# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "reviews")
VIDEO_DIR = os.path.join(BASE_DIR, "static", "review_videos")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


# =========================
# API BLUEPRINT
# =========================
api_accessories = Blueprint(
    "api_accessories",
    __name__,
    url_prefix="/api/accessories"
)


# =========================
# ADD ACCESSORY
# =========================
@api_accessories.route("/", methods=["POST"])
@jwt_required()
def add_accessory():
    data = request.get_json()

    accessory = {
        "name": data.get("name"),
        "price": data.get("price"),
        "description": data.get("description"),
        "category": data.get("category"),
        "image": data.get("image")
    }

    mongo.db.accessories.insert_one(accessory)

    return jsonify({"message": "Accessory added"}), 201


# =========================
# GET ALL ACCESSORIES
# =========================
@api_accessories.route("/", methods=["GET"])
def get_accessories():
    accessories = list(mongo.db.accessories.find())

    for a in accessories:
        a["id"] = str(a["_id"])
        del a["_id"]

    return jsonify(accessories)


# =========================
# GET SINGLE ACCESSORY
# =========================
@api_accessories.route("/<id>")
def get_accessory(id):
    a = mongo.db.accessories.find_one({"_id": ObjectId(id)})

    if not a:
        return jsonify({"error": "Not found"}), 404

    a["id"] = str(a["_id"])
    del a["_id"]

    return jsonify(a)


# =========================
# FRONTEND BLUEPRINT
# =========================
accessories_site = Blueprint("accessories_site", __name__)


@accessories_site.route("/accessories")
@accessories_site.route("/accessories.html")
def accessories_page():
    accessories = list(mongo.db.accessories.find())
    return render_template("accessories.html", accessories=accessories)


# =========================
# ACCESSORY DETAIL PAGE
# =========================
@accessories_site.route("/accessory/<id>")
def accessory_page(id):

    a = mongo.db.accessories.find_one({"_id": ObjectId(id)})

    if not a:
        return "Accessory Not Found", 404

    reviews = list(
        mongo.db.reviews.find(
            {"product_id": id}
        ).sort("_id", -1)
    )

    related = list(
        mongo.db.accessories.find({
            "category": a.get("category"),
            "_id": {"$ne": ObjectId(id)}
        }).limit(10)
    )

    # 🔥 Smart Fish Recommendation
    name_lower = a.get("name", "").lower()

    if "light" in name_lower or "led" in name_lower:
        fishes = list(
            mongo.db.products.find(
                {"category": "Planted"}
            ).limit(10)
        )
    elif "filter" in name_lower:
        fishes = list(
            mongo.db.products.find(
                {"category": "Community"}
            ).limit(10)
        )
    else:
        fishes = list(mongo.db.products.find().limit(10))

    return render_template(
        "accessory.html",
        a=a,
        related=related,
        fish_reco=fishes,
        reviews=reviews
    )


# =========================
# ADD REVIEW
# =========================
@api_accessories.route("/add-review", methods=["POST"])
def add_review():

    form = request.form
    images = request.files.getlist("images")
    video = request.files.get("video")

    img_names = []

    for img in images:
        if img.filename:
            name = f"{uuid.uuid4()}.{img.filename.rsplit('.',1)[1]}"
            img.save(os.path.join(IMAGE_DIR, name))
            img_names.append(name)

    video_name = None
    if video and video.filename:
        video_name = f"{uuid.uuid4()}.{video.filename.rsplit('.',1)[1]}"
        video.save(os.path.join(VIDEO_DIR, video_name))

    review = {
        "product_id": form.get("product_id"),
        "name": form.get("name"),
        "rating": int(form.get("rating")),
        "comment": form.get("comment"),
        "images": img_names,
        "video": video_name,
        "likes": 0
    }

    mongo.db.reviews.insert_one(review)

    return jsonify({"message": "Review added"})
