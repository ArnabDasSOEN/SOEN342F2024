"""
This module defines the Quotation class, which represents a price quotation
for a specific delivery request.
"""

from dbconnection import db


class Quotation(db.Model):
    """
    The Quotation class represents a price quotation for a specific delivery request.
    It includes a reference to the delivery request and the quoted price.
    """

    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    delivery_request_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_requests.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # pylint: disable=too-few-public-methods
    def __init__(self, delivery_request_id, price):
        """
        Initialize a Quotation instance.

        Args:
            delivery_request_id (int): The ID of the associated delivery request.
            price (float): The quoted price for the delivery request.
        """
        self.delivery_request_id = delivery_request_id
        self.price = price
