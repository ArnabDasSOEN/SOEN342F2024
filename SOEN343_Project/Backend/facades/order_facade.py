# facades/order_facade.py

from models.logistics.order import Order
from models.logistics.tracker import Tracker
from services.delivery_agent_service import DeliveryAgentService
from dbconnection import db


class OrderFacade:
    def __init__(self, order_controller=None, delivery_controller=None, payment_controller=None):
        self.order_controller = order_controller
        self.delivery_controller = delivery_controller
        self.payment_controller = payment_controller

    def create_order(self, delivery_request_id, customer_id):
        # Create a new order using delivery_request_id and customer_id
        order = Order(
            delivery_request_id=delivery_request_id,
            customer_id=customer_id,
            status="Processing"
        )
        db.session.add(order)
        db.session.commit()

        # Optionally assign a delivery agent and create a tracker
        delivery_agent = self.assign_delivery_agent(order)
        if delivery_agent:
            tracker = Tracker(
                order_id=order.id,
                delivery_agent_id=delivery_agent.id,
                status="In Transit"
            )
            db.session.add(tracker)
            db.session.commit()

        return order

    def assign_delivery_agent(self, order):
        # Use DeliveryAgentService to get a single delivery agent
        delivery_agent = DeliveryAgentService.assign_delivery_agent()
        if delivery_agent:
            # Assign the selected delivery agent to the order
            order.delivery_agent_id = delivery_agent.id
            db.session.commit()
            return delivery_agent
        else:
            print("No available delivery agents.")
            return None
