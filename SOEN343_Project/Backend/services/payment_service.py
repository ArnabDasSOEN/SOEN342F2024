from square.client import Client
import os
import uuid

class PaymentService:
    @staticmethod
    def process_payment(delivery_request_id, payment_method, amount):
        """
        Process a payment using the Square Payments API.

        :param delivery_request_id: Unique ID of the delivery request.
        :param payment_method: The payment token from the frontend.
        :param amount: The amount to be charged (in dollars).
        :return: True if payment is successful, False otherwise.
        """
        # Get the Squareup access token from environment variables
        squareup_access_token = os.getenv("SQUAREUP_ACCESS_TOKEN")
        #print("=-=-=-=-=-=-=-", squareup_access_token)
        if not squareup_access_token:
            raise ValueError("Squareup access token not found in environment variables. Please set SQUAREUP_ACCESS_TOKEN.")

        # Initialize the Square client
        square_client = Client(
            access_token=squareup_access_token,
            environment="sandbox"  # Change to "production" for live transactions
        )

        # Generate a unique idempotency key (max 45 chars)
        idempotency_key = f"del-{delivery_request_id}-{uuid.uuid4().hex[:10]}"

        # Create the payment request body
        body = {
            "source_id": payment_method,  # Payment token from the frontend
            "idempotency_key": idempotency_key,  # Unique key
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
            elif result.is_error():
                print("Payment failed:", result.errors)
                return False
        except Exception as e:
            print(f"Error during payment processing: {e}")
            return False
