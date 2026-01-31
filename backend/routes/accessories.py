import os, uuid
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required
from extensions import db
from models.accessory import Accessory
from models.review import Review
from models.product import Product   # fish model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "reviews")
VIDEO_DIR = os.path.join(BASE_DIR, "static", "review_videos")
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# =======================
# API BLUEPRINT
# =======================
api_accessories = Blueprint("api_accessories", __name__, url_prefix="/api/accessories")

@api_accessories.route("/", methods=["POST"])
@jwt_required()
def add_accessory():
    data = request.get_json()
    a = Accessory(**data)
    db.session.add(a)
    db.session.commit()
    return jsonify({"message":"Accessory added"}),201

@api_accessories.route("/", methods=["GET"])
def get_accessories():
    return jsonify([{
        "id":a.id,"name":a.name,"price":a.price,
        "description":a.description,"category":a.category
    } for a in Accessory.query.all()])

@api_accessories.route("/<int:id>")
def get_accessory(id):
    a = Accessory.query.get_or_404(id)
    return jsonify({
        "id":a.id,"name":a.name,"price":a.price,
        "description":a.description,"category":a.category
    })

# =======================
# FRONTEND BLUEPRINT
# =======================
accessories_site = Blueprint("accessories_site", __name__)

@accessories_site.route("/accessories")
@accessories_site.route("/accessories.html")
def accessories_page():
    return render_template("accessories.html", accessories=Accessory.query.all())

@accessories_site.route("/accessory/<int:id>")
def accessory_page(id):
    a = Accessory.query.get_or_404(id)
    reviews = Review.query.filter_by(product_id=id).order_by(Review.id.desc()).all()

    # Related accessories
    related = Accessory.query.filter(
        Accessory.category==a.category,
        Accessory.id!=id
    ).limit(10).all()

    # 🧠 Smart Fish Recommendation (based on category)
    if "light" in a.name.lower() or "led" in a.name.lower():
        fishes = Product.query.filter(Product.category=="Planted").limit(10).all()
    elif "filter" in a.name.lower():
        fishes = Product.query.filter(Product.category=="Community").limit(10).all()
    else:
        fishes = Product.query.limit(10).all()

    return render_template(
        "accessory.html",
        a=a,
        related=related,
        fish_reco=fishes,
        reviews=reviews
    )


# =======================
# REVIEWS
# =======================
@api_accessories.route("/add-review", methods=["POST"])
def add_review():
    form = request.form
    images = request.files.getlist("images")
    video = request.files.get("video")

    img_names=[]
    for img in images:
        if img.filename:
            name=f"{uuid.uuid4()}.{img.filename.rsplit('.',1)[1]}"
            img.save(os.path.join(IMAGE_DIR,name))
            img_names.append(name)

    video_name=None
    if video and video.filename:
        video_name=f"{uuid.uuid4()}.{video.filename.rsplit('.',1)[1]}"
        video.save(os.path.join(VIDEO_DIR,video_name))

    review = Review(
        product_id=form["product_id"],
        name=form["name"],
        rating=form["rating"],
        comment=form["comment"],
        images=",".join(img_names),
        video=video_name,
        likes=0
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message":"Review added"})


