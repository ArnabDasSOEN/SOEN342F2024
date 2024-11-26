"""
Payment Service
Handles payment processing using the Square Payments API.
"""

import os
import uuid
from square.client import Client


class PaymentService:
    """
    A service class to process payments using the Square Payments API.
    """

    @staticmethod
    def process_payment(delivery_request_id: str, payment_method: str, amount: float) -> bool:
        """
        Processes a payment using the Square Payments API.

        Args:
            delivery_request_id (str): Unique ID of the delivery request.
            payment_method (str): The payment token from the frontend.
            amount (float): The amount to be charged (in dollars).

        Returns:
            bool: True if payment is successful, False otherwise.

        Raises:
            ValueError: If the Squareup access token is not found in environment variables.
        """
        # Retrieve the Squareup access token
        squareup_access_token = os.getenv("SQUAREUP_ACCESS_TOKEN")
        if not squareup_access_token:
            raise ValueError(
                "Squareup access token not found in environment variables. Please set SQUAREUP_ACCESS_TOKEN.")

        # Initialize the Square client
        square_client = Client(
            access_token=squareup_access_token,
            environment="sandbox"  # Change to "production" for live transactions
        )

        # Generate a unique idempotency key (max 45 characters)
        idempotency_key = f"del-{delivery_request_id}-{uuid.uuid4().hex[:10]}"

        # Create the payment request body
        body = {
            "source_id": payment_method,  # Payment token from the frontend
            "idempotency_key": idempotency_key,
            "amount_money": {
                "amount": int(amount * 100),  # Convert dollars to cents
                "currency": "CAD"
            }
        }

        try:
            # Process the payment
            result = square_client.payments.create_payment(body)
            if result.is_success():
                print("Payment successful:", result.body)
                return True
            if result.is_error():
                print("Payment failed:", result.errors)
                return False
        except Exception as e:
            print(f"Error during payment processing: {e}")
            return False
