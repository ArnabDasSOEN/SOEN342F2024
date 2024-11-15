# controller/logistics_controller/delivery_controller.py

from flask import Blueprint, request, jsonify
from Models.Logistics.Tracker import Tracker, DeliveryStatus

delivery_agent_blueprint = Blueprint(
    'delivery_agent', __name__, url_prefix='/delivery_agent')


@delivery_agent_blueprint.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    tracker_id = data.get('tracker_id')
    new_status = data.get('status')

    # Retrieve tracker by ID
    tracker = Tracker.query.get(tracker_id)
    if tracker:
        # Validate new status against DeliveryStatus Enum
        status_enum = DeliveryStatus[new_status.upper()] if new_status.upper(
        ) in DeliveryStatus.__members__ else None
        if status_enum:
            # Call tracker's own update method
            tracker.update_status(status_enum)
            return jsonify({"status": "Tracker status and order status updated successfully"}), 200
        else:
            return jsonify({"error": "Invalid status provided"}), 400
    else:
        return jsonify({"error": "Tracker not found"}), 404
