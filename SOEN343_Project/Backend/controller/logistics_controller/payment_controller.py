# controller/logistics_controller/payment_controller.py

from flask import Blueprint, request, jsonify, current_app

payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.route('/make_payment', methods=['POST'])
def make_payment():
    data = request.json
    delivery_request_id = data.get('delivery_request_id')
    payment_method = data.get('payment_method')

    try:
        payment_facade = current_app.config['payment_facade']
        success = payment_facade.process_payment_and_create_order(
            delivery_request_id, payment_method)

        if success:
            return jsonify({"status": "Payment successful and order processed"}), 200
    except ValueError as e:
        # Handle known errors like "already paid"
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "Payment processing failed"}), 500

