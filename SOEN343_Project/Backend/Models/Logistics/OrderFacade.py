from .Order import Order
from .Tracker import Tracker


class OrderFacade:
    def __init__(self, payment_controller, delivery_controller, order_controller):
        self.payment_controller = payment_controller
        self.delivery_controller = delivery_controller
        self.order_controller = order_controller

    # OrderFacade.py

    def process_payment_and_create_order(self, delivery_request_id, payment_method):
        # 1. Process Payment
        payment_success = self.payment_controller.process_payment(
            delivery_request_id, payment_method
        )

        if not payment_success:
            return False

    # 2. Retrieve existing DeliveryRequest
        # creating test delivery_request
        d2 = self.delivery_controller.create_delivery_request(1, 1)
        delivery_request = self.delivery_controller.get_delivery_request_by_id(
            delivery_request_id
        )
        if not delivery_request:
            return False

    # Extract customer_id and delivery_request_id for the Order
        if isinstance(delivery_request, dict):
            customer_id = delivery_request.get('customer_id')
        else:
            customer_id = delivery_request.customer_id

    # 3. Create Order
        order = self.order_controller.create_order(
            delivery_request_id, customer_id)

    # 4. Assign Delivery Agent
        delivery_agent = self.delivery_controller.assign_delivery_agent(order)
        self.order_controller.assign_delivery_agent(order, delivery_agent)

    # 5. Create and Assign Tracker
        tracker = self.order_controller.create_tracker(order, delivery_agent)
        self.order_controller.assign_tracker(order, tracker)

        # 6. Notify Customer
        self.delivery_controller.notify_customer_with_tracking(
            order.customer_id, tracker
        )

        return True
