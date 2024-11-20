from flask import Blueprint, request, jsonify, current_app

payment_blueprint = Blueprint('payment', __name__, url_prefix='/payment')


@payment_blueprint.route('/make_payment', methods=['POST'])
def make_payment():
    data = request.json
    delivery_request_id = data.get('delivery_request_id')
    payment_method = data.get('payment_method')

    if not delivery_request_id or not payment_method:
        return jsonify({"error": "Delivery request ID and payment method are required."}), 400

    try:
        payment_facade = current_app.config['payment_facade']
        success = payment_facade.process_payment_and_create_order(
            delivery_request_id, payment_method)

        if success:
            return jsonify({"status": "Payment successful and order processed"}), 200
        else:
            return jsonify({"error": "Payment processing failed"}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Payment processing failed"}), 500


@payment_blueprint.route('/payment_history', methods=['POST'])
def payment_history():
    """
    Get payment history for a specific customer.
    Expects JSON data: { "user_id": <user_id> }
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
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve payment history: {e}"}), 500


@payment_blueprint.route('/payment_status', methods=['POST'])
def payment_status():
    """
    Get the status of a payment by order ID.
    Expects JSON data: { "order_id": <order_id> }
    """
    data = request.json
    order_id = data.get('order_id')

    if not order_id:
        return jsonify({"error": "Order ID is required."}), 400

    try:
        # Fetch payment status using order_id
        payment_status = current_app.config['payment_facade'].get_payment_status_by_order(
            order_id)
        if not payment_status:
            return jsonify({"message": "No payment found for the given Order ID"}), 404
        return jsonify(payment_status), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve payment status: {e}"}), 500
