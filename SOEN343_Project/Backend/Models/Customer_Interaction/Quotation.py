from dbconnection import db


class Quotation(db.Model):
    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    delivery_request_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_requests.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, delivery_request_id, price):
        self.delivery_request_id = delivery_request_id
        self.price = price
