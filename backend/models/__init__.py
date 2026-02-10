

# from extensions import db
# from .product import Product
# from .user import User
# from .cart import Cart
# from .order import Order
# from .accessory import Accessory
# from .accessory_review import AccessoryReview
from ..extensions import mongo

# Use functions to access collections AFTER Flask app is initialized
def users_collection():
    return mongo.db.user

def products_collection():
    return mongo.db.product

def carts_collection():
    return mongo.db.cart

def orders_collection():
    return mongo.db.order

def accessories_collection():
    return mongo.db.accessory

def accessory_reviews_collection():
    return mongo.db.accessory_review




