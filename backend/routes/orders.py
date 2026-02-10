@orders_bp.route("/", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()

    cart_items = list(mongo.db.cart.find({
        "user_id": ObjectId(user_id)
    }))

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = mongo.db.products.find_one(
            {"_id": item["product_id"]}
        )

        if item["quantity"] > product["stock"]:
            return jsonify({
                "message": f"Not enough stock for {product['name']}"
            }), 400

        total_amount += product["price"] * item["quantity"]

        order_items.append({
            "product_id": product["_id"],
            "quantity": item["quantity"],
            "price": product["price"]
        })

    order = {
        "user_id": ObjectId(user_id),
        "items": order_items,
        "total_amount": total_amount,
        "status": "pending"
    }

    mongo.db.orders.insert_one(order)

    mongo.db.cart.delete_many({
        "user_id": ObjectId(user_id)
    })

    return jsonify({
        "message": "Order created",
        "total_amount": total_amount
    }), 201
