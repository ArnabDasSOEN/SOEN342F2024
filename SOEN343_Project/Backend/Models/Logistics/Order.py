from dbconnection import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    delivery_request_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, delivery_request_id, customer_id, status="Pending"):
        self.delivery_request_id = delivery_request_id
        self.customer_id = customer_id
        self.status = status
