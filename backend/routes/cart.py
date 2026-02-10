from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from backend.extensions import mongo
from backend.models.cart import Cart

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


# =========================
# ADD TO CART
# =========================
@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"message": "Product ID required"}), 400

    # Check product exists
    product = mongo.db.products.find_one(
        {"_id": ObjectId(product_id)}
    )
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Check if already in cart
    existing_item = mongo.db.cart.find_one({
        "user_id": ObjectId(user_id),
        "product_id": ObjectId(product_id)
    })

    if existing_item:
        mongo.db.cart.update_one(
            {"_id": existing_item["_id"]},
            {"$inc": {"quantity": quantity}}
        )
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        mongo.db.cart.insert_one(cart_item.to_dict())

    return jsonify({"message": "Product added to cart"}), 200


# =========================
# GET CART ITEMS
# =========================
@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()

    cart_items = mongo.db.cart.find({
        "user_id": ObjectId(user_id)
    })

    result = []
    total_price = 0

    for item in cart_items:
        product = mongo.db.products.find_one(
            {"_id": item["product_id"]}
        )

        if not product:
            continue

        item_total = product["price"] * item["quantity"]
        total_price += item_total

        result.append({
            "cart_id": str(item["_id"]),
            "product_id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "quantity": item["quantity"],
            "image": product.get("image"),
            "item_total": item_total
        })

    return jsonify({
        "items": result,
        "total_price": total_price
    }), 200


# =========================
# REMOVE ITEM FROM CART
# =========================
@cart_bp.route("/remove/<cart_id>", methods=["DELETE"])
@jwt_required()
def remove_item(cart_id):
    user_id = get_jwt_identity()

    result = mongo.db.cart.delete_one({
        "_id": ObjectId(cart_id),
        "user_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        return jsonify({"message": "Cart item not found"}), 404

    return jsonify({"message": "Item removed from cart"}), 200


# =========================
# CLEAR CART
# =========================
@cart_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()

    mongo.db.cart.delete_many({
        "user_id": ObjectId(user_id)
    })

    return jsonify({"message": "Cart cleared"}), 200
