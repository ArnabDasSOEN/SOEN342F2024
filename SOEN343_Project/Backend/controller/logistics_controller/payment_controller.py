"""
This module defines endpoints for handling payment operations, including
making payments, retrieving payment history, and checking payment status.
"""

from flask import Blueprint, request, jsonify, current_app

payment_blueprint = Blueprint('payment', __name__, url_prefix='/payment')


@payment_blueprint.route('/make_payment', methods=['POST'])
def make_payment():
    """
    Process a payment and create an order.

    Expects JSON data:
    {
        "delivery_request_id": <int>,
        "payment_method": <str>
    }

    Returns:
        - 200: Payment successful and order processed.
        - 400: Missing required fields.
        - 500: Payment processing failed.
    """
    data = request.json
    delivery_request_id = data.get('delivery_request_id')
    payment_method = data.get('payment_method')

    if not delivery_request_id or not payment_method:
        return jsonify({"error": "Delivery request ID and payment method are required."}), 400

    try:
        payment_facade = current_app.config['payment_facade']
        success = payment_facade.process_payment_and_create_order(
            delivery_request_id, payment_method
        )

        if success:
            return jsonify({"status": "Payment successful and order processed"}), 200
        return jsonify({"error": "Payment processing failed"}), 500
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": f"Unexpected error: {error}"}), 500


@payment_blueprint.route('/payment_history', methods=['POST'])
def payment_history():
    """
    Get payment history for a specific customer.

    Expects JSON data:
    {
        "user_id": <int>
    }

    Returns:
        - 200: Payment history retrieved successfully.
        - 400: Missing user ID.
        - 404: No payments found for the customer.
        - 500: Failed to retrieve payment history.
    """
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "Customer ID is required."}), 400

    try:
        payments = current_app.config['payment_facade'].get_payment_history(
            user_id)
        if not payments:
            return jsonify({"message": f"No payments found for customer ID {user_id}"}), 404
        return jsonify(payments), 200
    except KeyError as error:
        return jsonify({"error": f"Invalid data: {error}"}), 400
    except RuntimeError as error:
        return jsonify({"error": f"Failed to retrieve payment history: {error}"}), 500


@payment_blueprint.route('/payment_status', methods=['POST'])
def payment_status():
    """
    Get the status of a payment by order ID.

    Expects JSON data:
    {
        "order_id": <int>
    }

    Returns:
        - 200: Payment status retrieved successfully.
        - 400: Missing order ID.
        - 404: No payment found for the order.
        - 500: Failed to retrieve payment status.
    """
    data = request.json
    order_id = data.get('order_id')

    if not order_id:
        return jsonify({"error": "Order ID is required."}), 400

    try:
        # Fetch payment status using order_id
        status = current_app.config['payment_facade'].get_payment_status_by_order(
            order_id)
        if not status:
            return jsonify({"message": "No payment found for the given Order ID"}), 404
        return jsonify(status), 200
    except KeyError as error:
        return jsonify({"error": f"Invalid data: {error}"}), 400
    except RuntimeError as error:
        return jsonify({"error": f"Failed to retrieve payment status: {error}"}), 500
