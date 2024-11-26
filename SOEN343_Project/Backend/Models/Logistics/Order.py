"""
This module defines the Order class, which represents an order in the system.
It includes relationships to customers, delivery agents, and observers for notifications.
"""

from dbconnection import db
from models.customer_interaction.customer import Customer
from models.communication.subject import Subject
from models.communication.observer import Observer


class Order(db.Model, Subject):
    """
    The Order class represents an order in the system, including relationships
    to customers, delivery agents, and observers for handling notifications.
    """

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    delivery_request_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)  # Foreign key to Customer
    status = db.Column(db.String(50), nullable=False, default="Pending")
    delivery_agent_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_agents.id'), nullable=True)

    # Relationships
    customer = db.relationship("Customer", back_populates="orders")
    delivery_agent = db.relationship("DeliveryAgent", back_populates="orders")
    _observers = db.relationship(
        "Notification", backref="order", cascade="all, delete-orphan")

    def __init__(self, delivery_request_id: int, customer_id: int, delivery_agent_id: int = None, status: str = "Pending"):
        """
        Initialize an Order instance.

        Args:
            delivery_request_id (int): The ID of the related delivery request.
            customer_id (int): The ID of the customer placing the order.
            delivery_agent_id (int, optional): The ID of the assigned delivery agent. Defaults to None.
            status (str, optional): The status of the order. Defaults to "Pending".
        """
        self.delivery_request_id = delivery_request_id
        self.customer_id = customer_id
        self.delivery_agent_id = delivery_agent_id
        self.status = status

    def attach(self, observer: Observer):
        """
        Attach an observer to the order.

        Args:
            observer (Observer): The observer to attach.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            db.session.add(observer)

    def detach(self, observer: Observer):
        """
        Detach an observer from the order.

        Args:
            observer (Observer): The observer to detach.
        """
        if observer in self._observers:
            self._observers.remove(observer)
            db.session.delete(observer)

    def notify_observers(self):
        """
        Notify all observers of a status change.
        """
        for observer in self._observers:
            observer.update(self.status)

    def update_status(self, new_status: str):
        """
        Update the order's status and notify observers.

        Args:
            new_status (str): The new status of the order.
        """
        self.status = new_status
        db.session.commit()  # Commit the status update

        # Reload notifications to ensure they're attached to the session
        db.session.refresh(self)
        self.notify_observers()
