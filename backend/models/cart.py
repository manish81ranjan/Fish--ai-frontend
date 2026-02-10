from datetime import datetime
from bson import ObjectId


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
        # Store IDs as ObjectId in DB
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.product_id = ObjectId(product_id) if isinstance(product_id, str) else product_id
        self.quantity = int(quantity)
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
            "user_id": str(cart["user_id"]),
            "product_id": str(cart["product_id"]),
            "quantity": cart["quantity"],
            "created_at": cart["created_at"]
        }
