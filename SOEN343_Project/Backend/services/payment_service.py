# services/payment_service.py

class PaymentService:
    @staticmethod
    def process_payment(delivery_request_id, payment_method, amount):
        # Simulate payment processing logic
        print(f"Processing payment for DeliveryRequest {
              delivery_request_id} with method {payment_method} and amount {amount}")
        return True  # Assume payment is always successful for simplicity
