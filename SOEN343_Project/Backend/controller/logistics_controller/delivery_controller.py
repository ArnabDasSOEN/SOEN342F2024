from flask import Blueprint, request, jsonify, current_app
from models.logistics.tracker import Tracker, DeliveryStatus
from models.logistics.order import Order
from services.delivery_progress_simulator import start_simulation

delivery_agent_blueprint = Blueprint(
    'delivery_agent', __name__, url_prefix='/delivery_agent')


@delivery_agent_blueprint.route('/update_status', methods=['POST'])
def update_status():
    """
    Update the status of a delivery tracker.
    """
    data = request.json
    tracker_id = data.get('tracker_id')
    new_status = data.get('status')

    tracker = Tracker.query.get(tracker_id)
    if not tracker:
        return jsonify({"error": "Tracker not found"}), 404

    normalized_status = new_status.strip().upper().replace(" ", "_")
    status_enum = DeliveryStatus[normalized_status] if normalized_status in DeliveryStatus.__members__ else None

    if not status_enum:
        return jsonify({"error": "Invalid status provided"}), 400

    if status_enum == DeliveryStatus.OUT_FOR_DELIVERY:
        # Pass the app instance explicitly
        start_simulation(current_app._get_current_object(), tracker_id)

    tracker.update_status(status_enum)
    return jsonify({"status": f"Tracker status updated to {new_status}"}), 200


@delivery_agent_blueprint.route('/track', methods=['POST'])
def track_delivery():
    """
    Get the current status and estimated delivery time for a tracker by order_id.
    Expects JSON data: { "order_id": <order_id> }
    """
    data = request.json
    order_id = data.get('order_id')

    if not order_id:
        return jsonify({"error": "Order ID is required"}), 400

    # Find tracker associated with the order
    tracker = Tracker.query.filter_by(order_id=order_id).first()
    if not tracker:
        return jsonify({"error": "Tracker not found for the given Order ID"}), 404

    if tracker.status == DeliveryStatus.DELIVERED.value:
        return jsonify({
            "status": tracker.status,
            "message": "The delivery has been successfully completed."
        }), 200
    elif tracker.status == DeliveryStatus.OUT_FOR_DELIVERY.value:
        return jsonify({
            "status": tracker.status,
            "estimated_delivery_time": tracker.estimated_delivery_time,
            "message": "Delivery agent is en route to your destination."
        }), 200
    else:
        return jsonify({
            "status": tracker.status,
            "message": "Delivery agent is in transit."
        }), 200
