"""
This module provides routes for retrieving orders by user.
"""

from flask import Blueprint, request, jsonify
from models.logistics.order import Order

order_blueprint = Blueprint('order', __name__, url_prefix='/order')


@order_blueprint.route('/get_orders_by_user', methods=['POST'])
def get_orders_by_user():
    try:
        # Parse and validate JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        user_id = data.get('user_id')
        if not user_id or not isinstance(user_id, int):
            return jsonify({"error": "user_id is required and must be an integer"}), 400

        # Query orders based on user_id
        orders = Order.query.filter_by(customer_id=user_id).all()
        if not orders:
            return jsonify({"message": f"No orders found for user_id {user_id}"}), 404

        # Serialize orders
        serialized_orders = [
            {
                "order_id": order.id,
                "delivery_request_id": order.delivery_request_id,
                "status": order.status,
                "delivery_agent_id": order.delivery_agent_id,
                "customer_id": order.customer_id,
                "delivery_request": {
                    "pick_up_address": {
                        "street": getattr(order.delivery_request.pick_up_address, 'street', 'N/A'),
                        "house_number": getattr(order.delivery_request.pick_up_address, 'house_number', 'N/A'),
                        "city": getattr(order.delivery_request.pick_up_address, 'city', 'N/A'),
                        "country": getattr(order.delivery_request.pick_up_address, 'country', 'N/A'),
                    },
                    "drop_off_address": {
                        "street": getattr(order.delivery_request.drop_off_address, 'street', 'N/A'),
                        "house_number": getattr(order.delivery_request.drop_off_address, 'house_number', 'N/A'),
                        "city": getattr(order.delivery_request.drop_off_address, 'city', 'N/A'),
                        "country": getattr(order.delivery_request.drop_off_address, 'country', 'N/A'),
                    },
                } if order.delivery_request else "N/A",
            }
            for order in orders
        ]

        return jsonify(serialized_orders), 200

    except RuntimeError as runtime_err:
        # Explicitly catch RuntimeError for mocking test
        print(f"Runtime error occurred: {runtime_err}")
        return jsonify({"error": "An error occurred while fetching orders"}), 500

    except Exception as exc:
        # General fallback for unexpected errors
        print(f"Unexpected error occurred: {exc}")
        return jsonify({"error": "An unexpected error occurred"}), 500
