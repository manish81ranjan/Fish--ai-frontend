from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.cart import Cart
from models.product import Product

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")


# =========================
# ADD TO CART
# =========================
@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"message": "Product ID required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    cart_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({"message": "Product added to cart"}), 200


# =========================
# GET CART ITEMS
# =========================
@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    result = []
    total_price = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)

        if not product:
            continue

        item_total = product.price * item.quantity
        total_price += item_total

        result.append({
            "cart_id": item.id,
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "image": product.image,
            "item_total": item_total
        })

    return jsonify({
        "items": result,
        "total_price": total_price
    }), 200


# =========================
# REMOVE ITEM FROM CART
# =========================
@cart_bp.route("/remove/<int:cart_id>", methods=["DELETE"])
@jwt_required()
def remove_item(cart_id):
    user_id = get_jwt_identity()

    cart_item = Cart.query.filter_by(
        id=cart_id,
        user_id=user_id
    ).first()

    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Item removed from cart"}), 200


# =========================
# CLEAR CART
# =========================
@cart_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()

    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({"message": "Cart cleared"}), 200
