from datetime import datetime


class AccessoryReview:
    """
    MongoDB Accessory Review helper class
    """

    def __init__(
        self,
        product_id,
        name,
        rating,
        comment=None,
        images=None,
        video=None,
        created_at=None
    ):
        self.product_id = product_id          # stored as string (ObjectId)
        self.name = name
        self.rating = rating
        self.comment = comment
        self.images = images or []            # list of image URLs
        self.video = video
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        """
        Used when inserting into MongoDB
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "rating": self.rating,
            "comment": self.comment,
            "images": self.images,
            "video": self.video,
            "created_at": self.created_at
        }

    @staticmethod
    def serialize(review):
        """
        Used when sending data to frontend (JSON safe)
        """
        return {
            "id": str(review["_id"]),
            "product_id": review.get("product_id"),
            "name": review.get("name"),
            "rating": review.get("rating"),
            "comment": review.get("comment"),
            "images": review.get("images", []),
            "video": review.get("video"),
            "created_at": review.get("created_at")
        }
