from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from main import db
from extensions import db
from models.cart import Cart
from models.product import Product

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")

@cart_bp.route("/", methods=["POST"])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    user_id = get_jwt_identity()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    cart_item = Cart.query.filter_by(
        user_id=user_id, product_id=product_id
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

    return jsonify({"message": "Item added to cart"}), 200


@cart_bp.route("/", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    result = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        result.append({
            "cart_id": item.id,
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": product.price * item.quantity
        })

    return jsonify(result), 200


@cart_bp.route("/<int:cart_id>", methods=["PUT"])
@jwt_required()
def update_cart(cart_id):
    data = request.get_json()
    quantity = data.get("quantity")

    cart_item = Cart.query.get_or_404(cart_id)
    cart_item.quantity = quantity

    db.session.commit()

    return jsonify({"message": "Cart updated"}), 200

@cart_bp.route("/<int:cart_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Item removed from cart"}), 200

