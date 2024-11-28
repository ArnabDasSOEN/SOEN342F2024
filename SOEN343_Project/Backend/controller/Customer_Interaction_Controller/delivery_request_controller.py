"""
This module provides routes for managing delivery requests, including
creation, cancellation, updates, and retrieval of requests.
"""

from flask import Blueprint, request, jsonify, current_app
from models.logistics.delivery_request import DeliveryRequest
from models.customer_interaction.quotation import Quotation
from dbconnection import db

delivery_request_blueprint = Blueprint(
    'delivery_request', __name__, url_prefix='/delivery_request')


@delivery_request_blueprint.route('/create_delivery_request', methods=['POST'])
def create_delivery_request():
    """
    Create a new delivery request with an associated quotation.

    Expects JSON data:
    {
        "customer_id": <int>,
        "pick_up_address": <dict>,
        "drop_off_address": <dict>,
        "package": <dict>
    }

    Returns:
        - 201: Successfully created.
        - 400: Invalid input.
        - 500: Server error.
    """
    data = request.json

    required_fields = ["customer_id", "pick_up_address",
                       "drop_off_address", "package"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data["customer_id"], int):
        return jsonify({"error": "Invalid customer_id format"}), 400

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
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": f"Server error: {error}"}), 500


@delivery_request_blueprint.route('/cancel_delivery_request', methods=['POST'])
def cancel_delivery_request():
    """
    Cancel an existing delivery request.

    Expects JSON data:
    {
        "delivery_request_id": <int>
    }

    Returns:
        - 200: Successfully cancelled.
        - 400: Invalid input or request already cancelled/delivered.
        - 404: Delivery request not found.
        - 500: Server error.
    """
    data = request.json
    delivery_request_id = data.get("delivery_request_id")

    if not delivery_request_id or not isinstance(delivery_request_id, int):
        return jsonify({"error": "Invalid or missing delivery_request_id"}), 400

    try:
        delivery_request = DeliveryRequest.query.get(delivery_request_id)
        if not delivery_request:
            return jsonify({"error": "Delivery request not found"}), 404

        if delivery_request.status.lower() in ["cancelled", "delivered"]:
            return jsonify({"message": f"Cannot cancel delivery request in '{delivery_request.status}' state"}), 400

        delivery_request.status = "Cancelled"
        db.session.commit()
        return jsonify({"message": "Delivery request cancelled successfully"}), 200
    except RuntimeError as error:
        return jsonify({"error": f"Server error: {error}"}), 500


@delivery_request_blueprint.route('/view_delivery_requests', methods=['POST'])
def view_delivery_requests():
    """
    Retrieve all delivery requests for a specific user, including associated quotations.
    """
    data = request.json
    user_id = data.get("user_id")

    try:
        # Convert user_id to an integer if it's a string
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing user_id"}), 400

    try:
        # Query delivery requests for the user
        delivery_requests = DeliveryRequest.query.filter_by(customer_id=user_id).all()

        if not delivery_requests:
            return jsonify({"message": f"No delivery requests found for user_id {user_id}"}), 404

        # Serialize delivery requests with quotations
        serialized_requests = []
        for req in delivery_requests:
            # Fetch the associated quotation for the delivery request
            quotation = Quotation.query.filter_by(delivery_request_id=req.id).first()

            serialized_requests.append({
                "delivery_request_id": req.id,
                "status": req.status,
                "pick_up_address": {
                    "street": req.pick_up_address.street,
                    "house_number": req.pick_up_address.house_number,
                    "city": req.pick_up_address.city,
                    "country": req.pick_up_address.country
                },
                "drop_off_address": {
                    "street": req.drop_off_address.street,
                    "house_number": req.drop_off_address.house_number,
                    "city": req.drop_off_address.city,
                    "country": req.drop_off_address.country
                },
                "quotation": {
                    "id": quotation.id if quotation else None,
                    "price": quotation.price if quotation else None
                }
            })

        return jsonify(serialized_requests), 200

    except Exception as error:
        return jsonify({"error": f"Server error: {error}"}), 500


@delivery_request_blueprint.route('/update_delivery_request', methods=['POST'])
def update_delivery_request():
    """
    Update an existing delivery request.

    Expects JSON data:
    {
        "delivery_request_id": <int>,
        "pick_up_address": <dict>,  # Optional
        "drop_off_address": <dict>,  # Optional
        "package": <dict>  # Optional
    }

    Returns:
        - 200: Successfully updated.
        - 400: Invalid input or no data provided.
        - 500: Server error.
    """
    data = request.json
    delivery_request_id = data.get("delivery_request_id")

    if not delivery_request_id or not isinstance(delivery_request_id, int):
        return jsonify({"error": "Invalid or missing delivery_request_id"}), 400

    pick_up_address_data = data.get("pick_up_address")
    if pick_up_address_data and not isinstance(pick_up_address_data, dict):
        return jsonify({"error": "Invalid pick_up_address data"}), 400

    drop_off_address_data = data.get("drop_off_address")
    if drop_off_address_data and not isinstance(drop_off_address_data, dict):
        return jsonify({"error": "Invalid drop_off_address data"}), 400

    package_data = data.get("package")
    if package_data and not isinstance(package_data, dict):
        return jsonify({"error": "Invalid package data"}), 400

    if not (pick_up_address_data or drop_off_address_data or package_data):
        return jsonify({"error": "No update data provided"}), 400

    try:
        facade = current_app.config['delivery_request_facade']
        result = facade.update_delivery_request(
            delivery_request_id=delivery_request_id,
            pick_up_address_data=pick_up_address_data,
            drop_off_address_data=drop_off_address_data,
            package_data=package_data
        )
        return jsonify(result), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": f"Server error: {error}"}), 500
