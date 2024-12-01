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

    def _get_delivery_request(self, delivery_request_id):
        delivery_request = db.session.query(
            DeliveryRequest).get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found")
        return delivery_request

    def _get_quotation(self, delivery_request_id):
        quotation = db.session.query(Quotation).filter_by(
            delivery_request_id=delivery_request_id).first()
        if not quotation:
            raise ValueError("Quotation not found for the delivery request")
        return quotation

    def _create_order(self, delivery_request_id, customer_id):
        order = Order(
            delivery_request_id=delivery_request_id,
            customer_id=customer_id,
            status="Processing"
        )
        db.session.add(order)
        db.session.commit()
        return order

    def _create_payment(self, customer_id, order_id, amount):
        payment = Payment(
            customer_id=customer_id,
            order_id=order_id,
            amount=amount,
            payment_date=datetime.utcnow(),
            status="Completed"
        )
        db.session.add(payment)
        db.session.commit()
        return payment

    def _notify_payment_success(self, delivery_request_id, customer_id, order_id):
        self.event_dispatcher.dispatch_event("payment_successful", {
            "delivery_request_id": delivery_request_id,
            "customer_id": customer_id,
            "order_id": order_id
        })

    def process_payment_and_create_order(self, delivery_request_id, payment_method):
        # Retrieve DeliveryRequest
        delivery_request = self._get_delivery_request(delivery_request_id)

        if delivery_request.status.lower() == "paid":
            raise ValueError("This delivery request has already been paid")

        customer_id = delivery_request.customer_id
        quotation = self._get_quotation(delivery_request_id)
        amount = quotation.price

        # Step 1: Process the payment
        if not PaymentService.process_payment(delivery_request_id, payment_method, amount):
            return None  # Return None if payment fails

        # Step 2: Update delivery request status to "Paid"
        delivery_request.status = "Paid"
        db.session.commit()

        # Step 3: Create an Order
        order = self._create_order(delivery_request_id, customer_id)

        # Step 4: Create the Payment record
        self._create_payment(customer_id, order.id, amount)

        # Step 5: Notify OrderFacade
        self._notify_payment_success(
            delivery_request_id, customer_id, order.id)

        return order.id

    def get_payment_history(self, user_id):
        """
        Retrieve payment history for a specific customer.
        """
        payments = db.session.query(Payment).filter_by(
            customer_id=user_id).all()
        return [
            {
                "payment_id": payment.id,
                "order_id": payment.order_id,
                "amount": payment.amount,
                "payment_date": payment.payment_date.isoformat(),
                "status": payment.status
            }
            for payment in payments
        ] if payments else []

    def get_payment_status_by_order(self, order_id):
        """
        Retrieve the status of a specific payment.
        """
        payment = db.session.query(Payment).filter_by(
            order_id=order_id).first()
        return {
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "payment_date": payment.payment_date.isoformat(),
            "status": payment.status
        } if payment else None
