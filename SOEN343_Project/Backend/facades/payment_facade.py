# facades/payment_facade.py

from models.logistics.delivery_request import DeliveryRequest
from models.logistics.order import Order
from models.logistics.payment import Payment
from models.customer_interaction.quotation import Quotation
from services.payment_service import PaymentService
from dbconnection import db
from datetime import datetime


class PaymentFacade:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

    def process_payment_and_create_order(self, delivery_request_id, payment_method):
        # Retrieve DeliveryRequest and associated Customer ID
        delivery_request = db.session.query(
            DeliveryRequest).get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found")

        customer_id = delivery_request.customer_id

        # Retrieve the Quotation price for the delivery_request_id
        quotation = db.session.query(Quotation).filter_by(
            delivery_request_id=delivery_request_id).first()
        if not quotation:
            raise ValueError("Quotation not found for the delivery request")

        amount = quotation.price

        # Step 1: Process the payment
        payment_success = PaymentService.process_payment(
            delivery_request_id, payment_method, amount)

        if payment_success:
            # Step 2: Update delivery request status to "Paid"
            delivery_request.status = "Paid"
            db.session.commit()

            # Step 3: Create an Order for the paid DeliveryRequest
            order = Order(
                delivery_request_id=delivery_request_id,
                customer_id=customer_id,
                status="Processing"
            )
            db.session.add(order)
            db.session.commit()

            # Step 4: Create the Payment record associated with the order
            payment = Payment(
                customer_id=customer_id,
                order_id=order.id,
                amount=amount,
                payment_date=datetime.utcnow(),
                status="Completed"
            )
            db.session.add(payment)
            db.session.commit()

            # Step 5: Notify OrderFacade to complete the order setup
            self.event_dispatcher.dispatch_event("payment_successful", {
                "delivery_request_id": delivery_request_id,
                "customer_id": customer_id,
                "order_id": order.id
            })

        return payment_success
