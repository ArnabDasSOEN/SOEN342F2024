"""
This module defines the Payment class, which represents payments in the system.
It includes relationships to customers and orders, as well as payment details.
"""

from datetime import datetime
from dbconnection import db


class Payment(db.Model):
    """
    The Payment class represents a payment transaction in the system.
    It includes details such as the customer, order, amount, payment date, and status.
    """

    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

    # Relationships
    customer = db.relationship("Customer", back_populates="payments")
    order = db.relationship("Order", backref="payment", uselist=False)

    # pylint: disable=too-few-public-methods
    def __init__(self, **kwargs):
        """
        Initialize a Payment instance.

        Args:
            kwargs (dict): A dictionary of payment attributes, including:
                - customer_id (int): The ID of the customer making the payment.
                - order_id (int): The ID of the associated order.
                - amount (float): The payment amount.
                - payment_date (datetime, optional): The date of the payment.
                - status (str, optional): The payment status (default: "Pending").
        """
        self.customer_id = kwargs.get('customer_id')
        self.order_id = kwargs.get('order_id')
        self.amount = kwargs.get('amount')
        self.payment_date = kwargs.get('payment_date', datetime.utcnow())
        self.status = kwargs.get('status', "Pending")
