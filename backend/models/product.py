from bson.objectid import ObjectId


class Product:
    """
    MongoDB Product helper class
    (NOT a SQLAlchemy model)
    """

    def __init__(
        self,
        name,
        price,
        description=None,
        image=None,
        rating=4.5,
        category=None,
        stock=0
    ):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.rating = rating
        self.category = category
        self.stock = stock

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image,
            "rating": self.rating,
            "category": self.category,
            "stock": self.stock
        }

    @staticmethod
    def serialize(product):
        """
        Converts MongoDB document → JSON-safe dict
        """
        return {
            "id": str(product["_id"]),
            "name": product.get("name"),
            "price": product.get("price"),
            "description": product.get("description"),
            "image": product.get("image"),
            "rating": product.get("rating", 4.5),
            "category": product.get("category"),
            "stock": product.get("stock", 0)
        }
