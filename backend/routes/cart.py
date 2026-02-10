from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from backend.extensions import mongo

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


# =========================
# ADD TO CART
# =========================
@cart_bp.route("/", methods=["POST"])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    user_id = get_jwt_identity()

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"message": "Product ID required"}), 400

    # Check product exists
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Check existing cart item
    cart_item = mongo.db.cart.find_one({
        "user_id": user_id,
        "product_id": product_id
    })

    if cart_item:
        mongo.db.cart.update_one(
            {"_id": cart_item["_id"]},
            {"$inc": {"quantity": quantity}}
        )
    else:
        mongo.db.cart.insert_one({
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        })

    return jsonify({"message": "Item added to cart"}), 200


# =========================
# VIEW CART
# =========================
@cart_bp.route("/", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()

    cart_items = mongo.db.cart.find({"user_id": user_id})

    result = []

    for item in cart_items:
        product = mongo.db.products.find_one(
            {"_id": ObjectId(item["product_id"])}
        )

        if not product:
            continue

        result.append({
            "cart_id": str(item["_id"]),
            "product_id": item["product_id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": item["quantity"],
            "subtotal": product["price"] * item["quantity"]
        })

    return jsonify(result), 200


# =========================
# UPDATE CART ITEM
# =========================
@cart_bp.route("/<cart_id>", methods=["PUT"])
@jwt_required()
def update_cart(cart_id):
    data = request.get_json()
    quantity = int(data.get("quantity", 1))

    mongo.db.cart.update_one(
        {"_id": ObjectId(cart_id)},
        {"$set": {"quantity": quantity}}
    )

    return jsonify({"message": "Cart updated"}), 200


# =========================
# REMOVE FROM CART
# =========================
@cart_bp.route("/<cart_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(cart_id):
    mongo.db.cart.delete_one(
        {"_id": ObjectId(cart_id)}
    )

    return jsonify({"message": "Item removed from cart"}), 200
