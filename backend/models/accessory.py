from extensions import db

class Accessory(db.Model):
    __tablename__ = "accessories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    rating = db.Column(db.Float)
    category = db.Column(db.String(50))
