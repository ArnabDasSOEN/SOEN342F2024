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

        # Check if the DeliveryRequest is already paid
        if delivery_request.status.lower() == "paid":
            raise ValueError("This delivery request has already been paid")

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

    def get_payment_history(self, user_id):
        """
        Retrieve payment history for a specific customer.
        """
        payments = db.session.query(Payment).filter_by(
            customer_id=user_id).all()
        if not payments:
            return []
        return [
            {
                "payment_id": payment.id,
                "order_id": payment.order_id,
                "amount": payment.amount,
                "payment_date": payment.payment_date.isoformat(),
                "status": payment.status
            }
            for payment in payments
        ]

    def get_payment_status_by_order(self, order_id):
        """
        Retrieve the status of a specific payment.
        """
        payment = db.session.query(Payment).filter_by(
            order_id=order_id).first()
        if not payment:
            return None
        return {
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "payment_date": payment.payment_date.isoformat(),
            "status": payment.status
        }
