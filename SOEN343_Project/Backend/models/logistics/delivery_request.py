"""
This module defines the DeliveryRequest class, which represents a delivery request
in the system, including its customer, package, addresses, and status.
"""

from dbconnection import db
from models.customer_interaction.customer import Customer
from models.customer_interaction.address import Address
from models.logistics.package import Package


class DeliveryRequest(db.Model):
    """
    The DeliveryRequest class represents a delivery request, including its associated
    customer, package, pick-up and drop-off addresses, and current status.
    """

    __tablename__ = 'delivery_requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey(
        'packages.id', name='fk_delivery_requests_package_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Requested")

    # Foreign keys to Address table with explicit names
    pick_up_address_id = db.Column(db.Integer, db.ForeignKey(
        'addresses.id', name='fk_delivery_requests_pick_up_address_id'), nullable=False)
    drop_off_address_id = db.Column(db.Integer, db.ForeignKey(
        'addresses.id', name='fk_delivery_requests_drop_off_address_id'), nullable=False)

    # Relationships
    customer = db.relationship("Customer", back_populates="delivery_requests")
    pick_up_address = db.relationship(
        "Address", foreign_keys=[pick_up_address_id], backref="pickup_requests")
    drop_off_address = db.relationship(
        "Address", foreign_keys=[drop_off_address_id], backref="dropoff_requests")
    package = db.relationship(
        "Package", backref="delivery_requests", uselist=False)

    # pylint: disable=too-few-public-methods
