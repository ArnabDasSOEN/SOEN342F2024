# facades/order_facade.py

from models.logistics.order import Order
from models.logistics.tracker import Tracker
from services.delivery_agent_service import DeliveryAgentService
from services.notification_factory import NotificationFactory
from dbconnection import db


class OrderFacade:
    def __init__(self):
        pass  # No injected dependencies needed

    def finalize_order(self, order_id):
        # Retrieve the order using order_id
        order = db.session.query(Order).get(order_id)
        if not order:
            raise ValueError("Order not found")

        # Attach notifications based on customer preferences and add to session
        customer = order.customer
        if customer.email:
            email_notification = NotificationFactory.create_notification(
                "email", "Your order has been created.", customer.email, order_id=order_id
            )
            order.attach(email_notification)
            db.session.add(email_notification)  # Add to session

        if customer.phone_number:
            sms_notification = NotificationFactory.create_notification(
                "sms", "Your order has been created.", customer.phone_number, order_id=order_id
            )
            order.attach(sms_notification)
            db.session.add(sms_notification)  # Add to session

        # Commit the notifications to the database
        db.session.commit()

        # Assign a delivery agent
        delivery_agent = self.assign_delivery_agent(order)
        if delivery_agent:
            # Update the order status to "In Transit" using the update_status method
            order.update_status("In Transit")

            # Create a tracker for the order
            tracker = Tracker(
                order_id=order.id,
                delivery_agent_id=delivery_agent.id,
                status="In Transit"
            )
            db.session.add(tracker)
            db.session.commit()

    def assign_delivery_agent(self, order):
        # Use DeliveryAgentService to get a delivery agent
        delivery_agent = DeliveryAgentService.assign_delivery_agent()
        if delivery_agent:
            order.delivery_agent_id = delivery_agent.id
            db.session.commit()
            return delivery_agent
        else:
            print("No available delivery agents.")
            return None

