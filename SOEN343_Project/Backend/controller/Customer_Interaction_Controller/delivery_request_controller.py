# Controller/Customer_Interaction_Controller/delivery_request_controller.py
from flask import Blueprint, request, jsonify, current_app

delivery_request_blueprint = Blueprint('delivery_request', __name__)


@delivery_request_blueprint.route('/create_delivery_request', methods=['POST'])
def create_delivery_request():
    data = request.json

    try:
        # Access the DeliveryRequestFacade instance from app config
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
        return jsonify({"error": str(e)}), 400
