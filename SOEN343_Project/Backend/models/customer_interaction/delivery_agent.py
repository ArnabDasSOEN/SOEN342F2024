# models/customer_interaction/delivery_agent.py

from dbconnection import db
from .user import User
from models.logistics.tracker import Tracker  # Ensure Tracker is imported


class DeliveryAgent(User):
    __tablename__ = 'delivery_agents'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # Relationships with Order and Tracker using string references
    orders = db.relationship(
        "Order", back_populates="delivery_agent", lazy='dynamic')
    trackers = db.relationship(
        "Tracker", back_populates="delivery_agent", lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'deliveryagent',
    }

    def __init__(self, name, password, email, phone_number):
        super().__init__(name, password, email, phone_number)

    def update_tracker_status(self, tracker_id, new_status):
        # Retrieve the tracker by ID
        tracker = Tracker.query.get(tracker_id)

        # Check if the tracker is assigned to this delivery agent
        if tracker and tracker.delivery_agent_id == self.id:
            # Update the status of the tracker
            tracker.status = new_status.value
            db.session.commit()
            return True
        else:
            print("Tracker not found or not assigned to this delivery agent.")
            return False
