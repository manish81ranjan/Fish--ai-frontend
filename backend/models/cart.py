from datetime import datetime


class Cart:
    """
    MongoDB Cart helper class
    One document per product per user
    """

    def __init__(
        self,
        user_id,
        product_id,
        quantity=1,
        created_at=None
    ):
        self.user_id = user_id              # string (ObjectId)
        self.product_id = product_id        # string (ObjectId)
        self.quantity = quantity
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        """
        Used while inserting into MongoDB
        """
        return {
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at
        }

    @staticmethod
    def serialize(cart):
        """
        Used while sending data to frontend
        """
        return {
            "id": str(cart["_id"]),
            "user_id": cart.get("user_id"),
            "product_id": cart.get("product_id"),
            "quantity": cart.get("quantity"),
            "created_at": cart.get("created_at")
        }
