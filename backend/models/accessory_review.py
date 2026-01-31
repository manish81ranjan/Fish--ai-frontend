from extensions import db
from datetime import datetime

class AccessoryReview(db.Model):
    __tablename__ = "accessory_reviews"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    images = db.Column(db.Text)
    video = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
