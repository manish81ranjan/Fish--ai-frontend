from bson.objectid import ObjectId


class Accessory:
    """
    MongoDB Accessory helper class
    (No SQLAlchemy, no schema binding)
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
        """
        Used when inserting into MongoDB
        """
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
    def serialize(accessory):
        """
        Used when sending data to frontend (JSON safe)
        """
        return {
            "id": str(accessory["_id"]),
            "name": accessory.get("name"),
            "price": accessory.get("price"),
            "description": accessory.get("description"),
            "image": accessory.get("image"),
            "rating": accessory.get("rating", 4.5),
            "category": accessory.get("category"),
            "stock": accessory.get("stock", 0)
        }
