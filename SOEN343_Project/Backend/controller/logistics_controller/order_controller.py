# controller/logistics_controller/order_controller.py
from flask import Blueprint, request, jsonify, current_app
from models.logistics.order import Order

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/get_orders_by_user', methods=['POST'])
def get_orders_by_user():
    """
    Retrieve orders for a specific user based on user_id provided in the JSON body.
    """
    try:
        # Parse and validate JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        user_id = data.get('user_id')
        if not user_id or not isinstance(user_id, int):
            return jsonify({"error": "user_id is required and must be an integer"}), 400

        # Authorization (placeholder for actual implementation)
        # Uncomment and implement if you have an authorization layer
        # if not authorize_user(request.user, user_id):
        #     return jsonify({"error": "Unauthorized access"}), 403

        # Query orders based on user_id
        orders = Order.query.filter_by(customer_id=user_id).all()
        if not orders:
            return jsonify({"message": f"No orders found for user_id {user_id}"}), 404

        # Serialize orders
        serialized_orders = []
        for order in orders:
            try:
                serialized_orders.append({
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
                    },
                })
            except AttributeError as attr_err:
                print(f"Serialization error for order {order.id}: {attr_err}")
                continue

        return jsonify(serialized_orders), 200

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error fetching orders for user_id: {e}")
        return jsonify({"error": "An error occurred while fetching orders"}), 500
