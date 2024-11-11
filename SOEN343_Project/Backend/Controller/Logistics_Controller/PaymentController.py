class PaymentController:
    def process_payment(self, delivery_request_id, payment_method):
        # Simulate payment processing logic
        print(f"Processing payment for DeliveryRequest {
              delivery_request_id} with method {payment_method}")
        return True  # Simulate successful payment
