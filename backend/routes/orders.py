from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from main import db
from extensions import db
from models.order import Order
from models.cart import Cart
from models.product import Product
from models.order import Order

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@orders_bp.route("/", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total_amount = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if item.quantity > product.stock:
            return jsonify({
                "message": f"Not enough stock for {product.name}"
            }), 400

        total_amount += product.price * item.quantity

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        "message": "Order created",
        "order_id": order.id,
        "total_amount": total_amount
    }), 201


@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()

    orders = Order.query.filter_by(user_id=user_id).all()

    result = []
    for order in orders:
        result.append({
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at
        })

    return jsonify(result), 200


