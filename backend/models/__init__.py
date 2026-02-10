

# from extensions import db
# from .product import Product
# from .user import User
# from .cart import Cart
# from .order import Order
# from .accessory import Accessory
# from .accessory_review import AccessoryReview
from ..extensions import mongo

# Example: collections
users_collection = mongo.db.user
products_collection = mongo.db.product
carts_collection = mongo.db.cart
orders_collection = mongo.db.order
accessories_collection = mongo.db.accessory
accessory_reviews_collection = mongo.db.accessory_review



