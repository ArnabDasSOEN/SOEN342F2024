"""
This module provides routes for retrieving orders by user.
"""

from flask import Blueprint, request, jsonify
from models.logistics.order import Order

order_blueprint = Blueprint('order', __name__, url_prefix='/order')


@order_blueprint.route('/get_orders_by_user', methods=['POST'])
def get_orders_by_user():
    """
    Retrieve orders for a specific user based on user_id provided in the JSON body.

    Expects JSON payload:
    {
        "user_id": <int>
    }

    Returns:
        - 200: List of orders for the user.
        - 400: Invalid input.
        - 404: No orders found.
        - 500: Server error.
    """
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
        serialized_orders = []
        for order in orders:
            delivery_request = order.delivery_request
            serialized_orders.append({
                "order_id": order.id,
                "delivery_request_id": order.delivery_request_id,
                "status": order.status,
                "delivery_agent_id": order.delivery_agent_id,
                "customer_id": order.customer_id,
                "delivery_request": {
                    "pick_up_address": {
                        "street": getattr(delivery_request.pick_up_address, 'street', 'N/A'),
                        "house_number": getattr(delivery_request.pick_up_address, 'house_number', 'N/A'),
                        "city": getattr(delivery_request.pick_up_address, 'city', 'N/A'),
                        "country": getattr(delivery_request.pick_up_address, 'country', 'N/A'),
                    },
                    "drop_off_address": {
                        "street": getattr(delivery_request.drop_off_address, 'street', 'N/A'),
                        "house_number": getattr(delivery_request.drop_off_address, 'house_number', 'N/A'),
                        "city": getattr(delivery_request.drop_off_address, 'city', 'N/A'),
                        "country": getattr(delivery_request.drop_off_address, 'country', 'N/A'),
                    },
                } if delivery_request else "N/A",
            })


        return jsonify(serialized_orders), 200

    except AttributeError as attr_err:
        # Log attribute errors for debugging purposes
        print(f"Attribute error occurred: {attr_err}")
        return jsonify({"error": "Data serialization issue occurred"}), 500
    except RuntimeError as runtime_err:
        # Log runtime errors
        print(f"Runtime error: {runtime_err}")
        return jsonify({"error": "An error occurred while fetching orders"}), 500
