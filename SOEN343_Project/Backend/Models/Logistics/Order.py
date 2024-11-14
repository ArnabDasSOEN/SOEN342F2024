# models/logistics/order.py

from dbconnection import db
from models.customer_interaction.customer import Customer


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    delivery_request_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)  # Foreign key to Customer
    status = db.Column(db.String(50), nullable=False, default="Pending")
    delivery_agent_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_agents.id'), nullable=True)

    # Relationships
    # Define relationship to Customer
    customer = db.relationship("Customer", back_populates="orders")
    # Define relationship to DeliveryAgent
    delivery_agent = db.relationship("DeliveryAgent", back_populates="orders")

    def __init__(self, delivery_request_id, customer_id, delivery_agent_id=None, status="Pending"):
        self.delivery_request_id = delivery_request_id
        self.customer_id = customer_id
        self.delivery_agent_id = delivery_agent_id
        self.status = status
