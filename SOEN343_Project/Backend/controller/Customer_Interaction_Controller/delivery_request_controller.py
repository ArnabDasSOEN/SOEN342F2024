from flask import Blueprint, request, jsonify, current_app
from models.logistics.delivery_request import DeliveryRequest
from dbconnection import db

delivery_request_blueprint = Blueprint('delivery_request', __name__)


@delivery_request_blueprint.route('/create_delivery_request', methods=['POST'])
def create_delivery_request():
    data = request.json

    # Input validation
    if not all(key in data for key in ["customer_id", "pick_up_address", "drop_off_address", "package"]):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data["customer_id"], int):
        return jsonify({"error": "Invalid customer_id format"}), 400

    # Ensure addresses and package data are dictionaries
    if not isinstance(data["pick_up_address"], dict) or not isinstance(data["drop_off_address"], dict) or not isinstance(data["package"], dict):
        return jsonify({"error": "Invalid address or package data"}), 400

    try:
        facade = current_app.config['delivery_request_facade']
        result = facade.create_delivery_request_with_quotation(
            customer_id=data["customer_id"],
            pick_up_address_data=data["pick_up_address"],
            drop_off_address_data=data["drop_off_address"],
            package_data=data["package"]
        )
        return jsonify({
            "message": "Delivery request and quotation created successfully",
            "delivery_request_id": result["delivery_request_id"],
            "quotation_price": result["quotation_price"]
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@delivery_request_blueprint.route('/cancel_delivery_request', methods=['POST'])
def cancel_delivery_request():
    data = request.json

    # Input validation
    delivery_request_id = data.get("delivery_request_id")
    if not delivery_request_id or not isinstance(delivery_request_id, int):
        return jsonify({"error": "Invalid or missing delivery_request_id"}), 400

    try:
        delivery_request = DeliveryRequest.query.get(delivery_request_id)
        if not delivery_request:
            return jsonify({"error": "Delivery request not found"}), 404

        # Validate state
        if delivery_request.status.lower() in ["cancelled", "delivered"]:
            return jsonify({"message": f"Cannot cancel delivery request in '{delivery_request.status}' state"}), 400

        # Cancel the request
        delivery_request.status = "Cancelled"
        db.session.commit()

        return jsonify({"message": "Delivery request cancelled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_request_blueprint.route('/view_delivery_requests', methods=['POST'])
def view_delivery_requests():
    data = request.json

    # Input validation
    user_id = data.get("user_id")
    if not user_id or not isinstance(user_id, int):
        return jsonify({"error": "Invalid or missing user_id"}), 400

    try:
        delivery_requests = DeliveryRequest.query.filter_by(customer_id=user_id).all()
        if not delivery_requests:
            return jsonify({"message": f"No delivery requests found for user_id {user_id}"}), 404

        serialized_requests = [
            {
                "delivery_request_id": request.id,
                "status": request.status,
                "pick_up_address": {
                    "street": request.pick_up_address.street,
                    "house_number": request.pick_up_address.house_number,
                    "city": request.pick_up_address.city,
                    "country": request.pick_up_address.country
                },
                "drop_off_address": {
                    "street": request.drop_off_address.street,
                    "house_number": request.drop_off_address.house_number,
                    "city": request.drop_off_address.city,
                    "country": request.drop_off_address.country
                }
            } for request in delivery_requests
        ]

        return jsonify(serialized_requests), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

