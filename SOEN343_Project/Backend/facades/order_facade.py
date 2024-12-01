from models.logistics.order import Order
from models.logistics.tracker import Tracker
from services.delivery_agent_service import DeliveryAgentService
from services.notification_factory import NotificationFactory


class OrderFacade:
    def __init__(self, db_session, delivery_service=None, notification_factory=None):
        self.db = db_session
        self.delivery_service = delivery_service or DeliveryAgentService()
        self.notification_factory = notification_factory or NotificationFactory()

    def finalize_order(self, order_id):
        # Retrieve the order
        order = self._get_order(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        # Create and attach notifications
        self._attach_notifications(order)

        # Assign a delivery agent and update the order status
        delivery_agent = self._assign_delivery_agent(order)
        if delivery_agent:
            self._update_order_status(order, "In Transit")
            self._create_tracker(order, delivery_agent)

    def _get_order(self, order_id):
        return self.db.session.query(Order).get(order_id)

    def _attach_notifications(self, order):
        customer = order.customer
        notifications = []

        if customer.email:
            email_notification = self.notification_factory.create_notification(
                "email", "Your order has been created.", customer.email, order_id=order.id
            )
            notifications.append(email_notification)

        if customer.phone_number:
            sms_notification = self.notification_factory.create_notification(
                "sms", "Your order has been created.", customer.phone_number, order_id=order.id
            )
            notifications.append(sms_notification)

        for notification in notifications:
            order.attach(notification)
            self.db.session.add(notification)

        self.db.session.commit()

    def _assign_delivery_agent(self, order):
        delivery_agent = self.delivery_service.assign_delivery_agent()
        if delivery_agent:
            order.delivery_agent_id = delivery_agent.id
            self.db.session.commit()
        else:
            print("No available delivery agents.")
        return delivery_agent

    def _update_order_status(self, order, status):
        order.update_status(status)
        self.db.session.commit()

    def _create_tracker(self, order, delivery_agent):
        tracker = Tracker(
            order_id=order.id,
            delivery_agent_id=delivery_agent.id,
            status="In Transit"
        )
        self.db.session.add(tracker)
        self.db.session.commit()
