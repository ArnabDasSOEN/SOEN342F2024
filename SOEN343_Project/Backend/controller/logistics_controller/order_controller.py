#
from flask import Blueprint, request, jsonify, current_app

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/make_payment', methods=['POST'])
def make_payment():
    data = request.json
    delivery_request_id = data.get('delivery_request_id')
    payment_method = data.get('payment_method')

    order_facade = current_app.config['order_facade']
    success = order_facade.process_payment_and_create_order(
        delivery_request_id, payment_method)

    if success:
        return jsonify({"status": "Payment successful and order processed"}), 200
    else:
        return jsonify({"status": "Payment processing failed"}), 400
