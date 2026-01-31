from extensions import db
from datetime import datetime


class Review(db.Model):
    __tablename__ = "reviews"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)

    images = db.Column(db.Text)
    video = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # def __init__(self, product_id, name, rating, comment, image=None):
    #     self.product_id = product_id
    #     self.name = name
    #     self.rating = rating
    #     self.comment = comment
    #     self.image = image
