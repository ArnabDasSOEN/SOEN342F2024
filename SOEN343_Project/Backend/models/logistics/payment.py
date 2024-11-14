# models/logistics/payment.py

from dbconnection import db
from models.logistics.order import Order
from models.customer_interaction.customer import Customer
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Relationships
    customer = db.relationship("Customer", back_populates="payments")
    order = db.relationship("Order", backref="payment", uselist=False)

    def __init__(self, customer_id, order_id, amount, payment_date, status="Pending"):
        self.customer_id = customer_id
        self.order_id = order_id
        self.amount = amount
        self.payment_date = payment_date
        self.status = status
