# models/logistics/tracker.py

from dbconnection import db
from enum import Enum
from models.logistics.order import Order


class DeliveryStatus(Enum):
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"


ORDER_STATUS_MAPPING = {
    DeliveryStatus.IN_TRANSIT: "Processing",
    DeliveryStatus.OUT_FOR_DELIVERY: "Out for Delivery",
    DeliveryStatus.DELIVERED: "Completed"
}


class Tracker(db.Model):
    __tablename__ = 'trackers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    delivery_agent_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_agents.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False,
                       default=DeliveryStatus.IN_TRANSIT.value)

    # Relationships using string references
    order = db.relationship("Order", backref="tracker")
    delivery_agent = db.relationship(
        "DeliveryAgent", back_populates="trackers")

    def __init__(self, order_id, delivery_agent_id, status="In Transit"):
        self.order_id = order_id
        self.delivery_agent_id = delivery_agent_id
        self.status = status

    def update_status(self, new_status):
        # Update the tracker's status attribute
        self.status = new_status.value
        db.session.commit()

        # Update associated order's status using the mapped value
        order_status = ORDER_STATUS_MAPPING.get(new_status)
        if order_status and self.order:
            self.order.update_status(order_status)
