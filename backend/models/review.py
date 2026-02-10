from datetime import datetime


class Review:
    """
    MongoDB Review helper class
    Used for product reviews
    """

    def __init__(
        self,
        product_id,
        name,
        rating,
        comment,
        images=None,
        video=None,
        likes=0,
        created_at=None
    ):
        self.product_id = product_id        # string (ObjectId)
        self.name = name
        self.rating = rating
        self.comment = comment
        self.images = images or []          # list of image URLs
        self.video = video
        self.likes = likes
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
            "likes": self.likes,
            "created_at": self.created_at
        }

    @staticmethod
    def serialize(review):
        """
        Used when sending review data to frontend
        """
        return {
            "id": str(review["_id"]),
            "product_id": review.get("product_id"),
            "name": review.get("name"),
            "rating": review.get("rating"),
            "comment": review.get("comment"),
            "images": review.get("images", []),
            "video": review.get("video"),
            "likes": review.get("likes", 0),
            "created_at": review.get("created_at")
        }
