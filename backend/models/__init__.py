

# from extensions import db
# from .product import Product
# from .user import User
# from .cart import Cart
# from .order import Order
# from .accessory import Accessory
# from .accessory_review import AccessoryReview
from ..extensions import mongo

# Example: collections
users_collection = mongo.db.users
products_collection = mongo.db.products
carts_collection = mongo.db.carts
orders_collection = mongo.db.orders
accessories_collection = mongo.db.accessories
accessory_reviews_collection = mongo.db.accessory_reviews


