# models/logistics/tracker.py

from dbconnection import db
from enum import Enum
from models.logistics.order import Order


class DeliveryStatus(Enum):
    IN_TRANSIT = "IN TRANSIT"
    OUT_FOR_DELIVERY = "OUT FOR DELIVERY"
    DELIVERED = "DELIVERED"


ORDER_STATUS_MAPPING = {
    DeliveryStatus.IN_TRANSIT: "Processing",
    DeliveryStatus.OUT_FOR_DELIVERY: "OUT FOR DELIVERY",
    DeliveryStatus.DELIVERED: "Completed"
}


class Tracker(db.Model):
    __tablename__ = 'trackers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    delivery_agent_id = db.Column(db.Integer, db.ForeignKey('delivery_agents.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default=DeliveryStatus.IN_TRANSIT.value)
    estimated_delivery_time = db.Column(db.Float, nullable=True)  # In minutes

    # Relationships
    order = db.relationship("Order", backref="tracker")
    delivery_agent = db.relationship("DeliveryAgent", back_populates="trackers")

    def update_status(self, new_status, delivery_time=None):
        """
        Update tracker status and optionally set estimated delivery time.
        """
        self.status = new_status.value
        if delivery_time is not None:
            self.estimated_delivery_time = delivery_time
        db.session.commit()

        # Update associated order's status
        order_status = ORDER_STATUS_MAPPING.get(new_status)
        if order_status and self.order:
            self.order.update_status(order_status)
