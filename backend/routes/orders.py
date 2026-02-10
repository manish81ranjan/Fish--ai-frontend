from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from backend.extensions import mongo  # ✅ absolute import (VERY IMPORTANT)

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@orders_bp.route("/", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()

    # Fetch cart items for the user
    cart_items = list(
        mongo.db.cart.find({"user_id": ObjectId(user_id)})
    )

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = mongo.db.products.find_one(
            {"_id": item["product_id"]}
        )

        if not product:
            return jsonify({"message": "Product not found"}), 404

        if item["quantity"] > product.get("stock", 0):
            return jsonify({
                "message": f"Not enough stock for {product['name']}"
            }), 400

        price = product["price"]
        quantity = item["quantity"]

        total_amount += price * quantity

        order_items.append({
            "product_id": product["_id"],
            "quantity": quantity,
            "price": price
        })

    # Create order document
    order = {
        "user_id": ObjectId(user_id),
        "items": order_items,
        "total_amount": total_amount,
        "status": "pending"
    }

    mongo.db.orders.insert_one(order)

    # Clear cart after order
    mongo.db.cart.delete_many({
        "user_id": ObjectId(user_id)
    })

    return jsonify({
        "message": "Order created successfully",
        "total_amount": total_amount
    }), 201
