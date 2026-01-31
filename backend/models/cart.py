# # from main import db
# from extensions import db


# class Cart(db.Model):
#     __tablename__ = "cart"

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
#     quantity = db.Column(db.Integer, default=1)

from extensions import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1)

