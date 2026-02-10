from datetime import datetime


class Order:
    """
    MongoDB Order helper class
    One document per order
    """

    def __init__(
        self,
        user_id,
        items,
        total_amount,
        status="pending",
        created_at=None
    ):
        self.user_id = user_id              # string (ObjectId)
        self.items = items                  # list of products
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        """
        Used while inserting into MongoDB
        """
        return {
            "user_id": self.user_id,
            "items": self.items,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at
        }

    @staticmethod
    def serialize(order):
        """
        Used while sending order data to frontend
        """
        return {
            "id": str(order["_id"]),
            "user_id": order.get("user_id"),
            "items": order.get("items", []),
            "total_amount": order.get("total_amount"),
            "status": order.get("status"),
            "created_at": order.get("created_at")
        }
