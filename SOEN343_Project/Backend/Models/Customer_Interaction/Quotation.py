from dbconnection import db

class Quotation:
    __tablename__ = 'quotations'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    quotationID = db.Column(db.String(50), nullable=False)

    def __init__(self, price, quotationID):
        self.price = price
        self.quotationID = quotationID