# controller/logistics_controller/delivery_controller.py

from flask import Blueprint, request, jsonify
from models.logistics.tracker import Tracker, DeliveryStatus
from services.distance_service import DistanceService
from models.logistics.delivery_request import DeliveryRequest

delivery_agent_blueprint = Blueprint(
    'delivery_agent', __name__, url_prefix='/delivery_agent')


@delivery_agent_blueprint.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    print(f"Incoming request data: {data}")

    tracker_id = data.get('tracker_id')
    new_status = data.get('status')

    tracker = Tracker.query.get(tracker_id)
    if tracker:
        normalized_status = new_status.strip().upper().replace(" ", "_")
        status_enum = DeliveryStatus[normalized_status] if normalized_status in DeliveryStatus.__members__ else None

        if status_enum:
            if status_enum == DeliveryStatus.IN_TRANSIT:
                delivery_request = DeliveryRequest.query.get(tracker.order.delivery_request_id)
                print(f"DeliveryRequest: {delivery_request}")
                print(f"Pickup Address: {delivery_request.pick_up_address}")
                print(f"Dropoff Address: {delivery_request.drop_off_address}")

                if not delivery_request:
                    return jsonify({"error": "Associated delivery request not found"}), 404

                try:
                    origin = f"{delivery_request.pick_up_address.street} {delivery_request.pick_up_address.house_number}, {delivery_request.pick_up_address.city}, {delivery_request.pick_up_address.country}"
                    destination = f"{delivery_request.drop_off_address.street} {delivery_request.drop_off_address.house_number}, {delivery_request.drop_off_address.city}, {delivery_request.drop_off_address.country}"

                    print(f"Calculating route time from: {origin} to {destination}")

                    travel_time = DistanceService.calculate_route_time(origin, destination)
                    print(f"Travel time calculated: {travel_time} minutes")

                    tracker.update_status(status_enum, delivery_time=travel_time)

                    return jsonify({
                        "status": "Tracker status updated to In Transit",
                        "estimated_delivery_time": travel_time
                    }), 200
                except Exception as e:
                    print(f"Error calculating route time: {e}")
                    return jsonify({"error": "Failed to calculate delivery time"}), 500
            else:
                tracker.update_status(status_enum)
                return jsonify({"status": "Tracker status updated"}), 200
        else:
            print("Invalid status provided.")
            return jsonify({"error": "Invalid status provided"}), 400
    else:
        print("Tracker not found.")
        return jsonify({"error": "Tracker not found"}), 404
