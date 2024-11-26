"""
This module defines the Tracker class and DeliveryStatus enum for managing
the tracking of orders and their statuses.
"""

from enum import Enum
from dbconnection import db


class DeliveryStatus(Enum):
    """
    DeliveryStatus is an enum representing possible statuses for a delivery.
    """
    IN_TRANSIT = "IN TRANSIT"
    OUT_FOR_DELIVERY = "OUT FOR DELIVERY"
    DELIVERED = "DELIVERED"


ORDER_STATUS_MAPPING = {
    DeliveryStatus.IN_TRANSIT: "Processing",
    DeliveryStatus.OUT_FOR_DELIVERY: "OUT FOR DELIVERY",
    DeliveryStatus.DELIVERED: "Completed"
}


class Tracker(db.Model):
    """
    Tracker represents the tracking information for an order, including its current
    status, associated delivery agent, and estimated delivery time.
    """
    __tablename__ = 'trackers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    delivery_agent_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_agents.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False,
                       default=DeliveryStatus.IN_TRANSIT.value)
    estimated_delivery_time = db.Column(db.Float, nullable=True)  # In minutes

    # Relationships
    order = db.relationship("Order", backref="tracker")
    delivery_agent = db.relationship(
        "DeliveryAgent", back_populates="trackers")

    # pylint: disable=too-few-public-methods
    def update_status(self, new_status: DeliveryStatus, delivery_time: float = None):
        """
        Update tracker status and optionally set estimated delivery time.

        Args:
            new_status (DeliveryStatus): The new delivery status.
            delivery_time (float, optional): The estimated time for delivery in minutes.
        """
        self.status = new_status.value
        if delivery_time is not None:
            self.estimated_delivery_time = delivery_time
        db.session.commit()

        print(f"Tracker {self.id} status updated to {
              self.status}, estimated delivery time: {self.estimated_delivery_time}")

        # Update associated order's status
        order_status = ORDER_STATUS_MAPPING.get(new_status)
        if order_status and self.order:
            self.order.update_status(order_status)
