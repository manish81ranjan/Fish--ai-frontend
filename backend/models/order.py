# from datetime import datetime
# # from main import db
# from extensions import db


# class Order(db.Model):
#     __tablename__ = "orders"

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     total_amount = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(50), default="pending")
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)


from extensions import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total = db.Column(db.Float)
