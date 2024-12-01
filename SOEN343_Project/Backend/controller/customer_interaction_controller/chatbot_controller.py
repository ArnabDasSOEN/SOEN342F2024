from flask import current_app
from flask import Blueprint, request, jsonify
import openai
from extensions import limiter  # Import limiter from extensions
from models.logistics.delivery_request import DeliveryRequest
from models.logistics.order import Order
from models.logistics.payment import Payment
import requests
import os
from flask_cors import CORS

# Initialize session state for conversations
session_state = {}

chatbot_blueprint = Blueprint('chatbot', __name__, url_prefix='/chatbot')
CORS(chatbot_blueprint)


@chatbot_blueprint.route('/ask', methods=['POST'])
# @limiter.limit("3 per minute")  # Apply rate limiting
def ask_chatbot(session_state_override=None):
    global session_state
    if session_state_override is not None:
        session_state = session_state_override
    """
    Handle user queries via chatbot with session-based flow.
    """
    data = request.json
    print("Received payload:", data)
    user_message = data.get("message")
    user_context = data.get("context", {})
    user_id = user_context.get("user_id")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    if not user_id:
        return jsonify({"error": "User ID is required in context"}), 400

    # Initialize session state if not already present
    if user_id not in session_state:
        session_state[user_id] = {"pending_command": None, "data": {}}

    try:
        # Handle follow-up for pending commands
        if session_state[user_id]["pending_command"] == "track_delivery":
            session_state[user_id]["pending_command"] = None
            return handle_track_delivery({**user_context, "order_id": user_message})

        if session_state[user_id]["pending_command"] == "check_payment_status":
            session_state[user_id]["pending_command"] = None
            return handle_payment_status({**user_context, "order_id": user_message})

        if session_state[user_id]["pending_command"] == "update_delivery_request":
            session_state[user_id]["pending_command"] = None
            return handle_update_delivery_request({**user_context, "delivery_request_id": user_message})

        if session_state[user_id]["pending_command"] == "cancel_delivery_request":
            session_state[user_id]["pending_command"] = None
            return handle_cancel_delivery_request({**user_context, "delivery_request_id": user_message})

        # Recognize new commands
        if "track my delivery" in user_message.lower():
            session_state[user_id]["pending_command"] = "track_delivery"
            return jsonify({"reply": "Please provide your order ID to track your delivery."}), 200

        if "check payment status" in user_message.lower():
            session_state[user_id]["pending_command"] = "check_payment_status"
            return jsonify({"reply": "Please provide your order ID to check payment status."}), 200

        if "create delivery request" in user_message.lower():
            return handle_create_delivery(user_context)

        if "update my delivery" in user_message.lower():
            return handle_update_delivery_request(user_context)

        if "cancel my delivery" in user_message.lower():
            session_state[user_id]["pending_command"] = "cancel_delivery_request"
            return jsonify({"reply": "Please provide the delivery request ID to cancel your delivery."}), 200

        if "view my payment history" in user_message.lower():
            return handle_view_payment_history(user_id)

        if "view my delivery requests" in user_message.lower():
            return handle_view_delivery_requests(user_id)

        # Fallback to GPT for general queries
        return fallback_to_gpt(user_message)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


def handle_track_delivery(user_context):
    """
    Handle tracking delivery requests.
    """
    order_id = user_context.get("order_id")
    if not order_id:
        return jsonify({"reply": "Please provide your order ID to track your delivery."}), 200

    response = requests.post(
        f"{request.host_url}delivery_agent/track",
        json={"order_id": order_id}
    )
    if response.status_code == 200:
        tracking_data = response.json()
        return jsonify({"reply": f"Your delivery status: {tracking_data['status']}. Estimated delivery time: {tracking_data.get('estimated_delivery_time', 'N/A')} minutes."}), 200
    elif response.status_code == 404:
        return jsonify({"reply": "Tracker not found for the given order ID."}), 404
    else:
        return jsonify({"reply": "Failed to fetch delivery status. Please ensure the order ID is correct."}), 500


def handle_payment_status(user_context):
    """
    Handle checking payment status.
    """
    order_id = user_context.get("order_id")
    if not order_id:
        return jsonify({"reply": "Please provide a valid Order ID from your payment history to check its status."}), 200

    response = requests.post(
        f"{request.host_url}payment/payment_status",
        json={"order_id": order_id}
    )
    if response.status_code == 200:
        payment_status = response.json()
        return jsonify({"reply": f"Payment Status: {payment_status['status']}, Amount: {payment_status['amount']}."}), 200
    else:
        return jsonify({"reply": "Failed to fetch payment status. Please ensure the Order ID is correct."}), 500


def handle_update_delivery_request(user_context):
    """
    Redirect to the delivery update page.
    """
    return jsonify({"reply": "navigate:update_delivery_request"}), 200


def handle_cancel_delivery_request(user_context):
    """
    Handle cancelling delivery requests.
    """
    delivery_request_id = user_context.get("delivery_request_id")
    if not delivery_request_id:
        return jsonify({"reply": "Please provide the delivery request ID to cancel your delivery."}), 200

    response = requests.post(
        f"{request.host_url}delivery_request/cancel",
        json={"delivery_request_id": delivery_request_id}
    )
    if response.status_code == 200:
        return jsonify({"reply": "Your delivery request has been cancelled successfully."}), 200
    else:
        return jsonify({"reply": "Failed to cancel delivery request. Please ensure the request ID is correct."}), 500


def fallback_to_gpt(user_message):
    """
    Fallback to OpenAI GPT for handling general queries.
    """
    openai_api_key = os.getenv("OPEN_AI_API_KEY")
    if not openai_api_key:
        return jsonify({"error": "OpenAI API key not configured"}), 500

    openai.api_key = openai_api_key
    response = openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": ("You are a helpful assistant for a delivery service. If a user asks for an unsupported query, "
                                           "list the options they can choose from:\n"
                                           "1. 'Track my delivery' to check delivery status (requires an order ID).\n"
                                           "2. 'View my payment history' to see payment details.\n"
                                           "3. 'Check payment status' for a specific order ID.\n"
                                           "4. 'Update my delivery' to modify a delivery request.\n"
                                           "5. 'Create delivery request' to schedule a delivery.\n"
                                           "6. 'Cancel my delivery' to cancel an existing delivery request.\n"
                                           "7. 'View my delivery requests' to see all current delivery requests.")},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=100
    )
    return jsonify({"reply": response.choices[0].message.content}), 200


def handle_view_payment_history(user_id=None):
    """
    Handle viewing payment history and prompt for payment ID to check its status.
    """
    print(user_id)  # Debug log for user ID
    if not user_id:
        return jsonify({"reply": "User ID is missing in the context. Please log in again."}), 401

    # Fetch payment history
    try:
        response = requests.post(
            f"{request.host_url}payment/payment_history",
            json={"user_id": user_id}
        )

        if response.status_code == 200:
            payments = response.json()
            if not payments:  # Check if the payments list is empty
                return jsonify({"reply": "You have no payments in your history."}), 200

            # Build a list of payments to display
            reply = "Here are your payments:\n"
            for payment in payments:
                reply += f"- Payment ID: {payment['payment_id']}, Amount: {
                    payment['amount']}, Status: {payment['status']}, Order ID: {payment['order_id']}\n"
            return jsonify({"reply": reply}), 200

        elif response.status_code == 404:  # Handle 404 status code explicitly
            return jsonify({"reply": "You have no payment history available."}), 200

        else:  # Catch other HTTP errors
            return jsonify({"reply": "Failed to fetch payment history. Please try again later."}), 500

    except requests.RequestException as e:  # Handle request errors
        print(f"Error fetching payment history: {e}")
        return jsonify({"reply": "An error occurred while fetching payment history. Please try again later."}), 500


def handle_view_delivery_requests(user_id):
    """
    Handle viewing delivery requests for the logged-in user.
    """
    print(user_id)  # Debug log for user ID
    if not user_id:
        return jsonify({"reply": "User ID is missing in the context. Please log in again."}), 401

    # Fetch delivery requests
    try:
        # Use current_app to get the base URL or construct the endpoint URL manually
        # Replace with your host configuration
        base_url = current_app.config.get("HOST_URL", "http://localhost:5000")
        endpoint_url = f"{base_url}/delivery_request/view_delivery_requests"

        response = requests.post(
            endpoint_url,
            json={"user_id": user_id}
        )

        if response.status_code == 200:
            delivery_requests = response.json()
            if not delivery_requests:  # Check if the delivery requests list is empty
                return jsonify({"reply": "You have no delivery requests."}), 200

            # Build a list of delivery requests to display
            reply = "Here are your delivery requests:\n"
            for req in delivery_requests:
                reply += f"- Request ID: {req['delivery_request_id']
                                          }, Status: {req['status']}\n"
            return jsonify({"reply": reply}), 200

        elif response.status_code == 404:  # Handle 404 status code explicitly
            return jsonify({"reply": "You have no delivery requests available."}), 200

        else:  # Catch other HTTP errors
            return jsonify({"reply": "Failed to fetch delivery requests. Please try again later."}), 500

    except requests.RequestException as e:  # Handle request errors
        print(f"Error fetching delivery requests: {e}")
        return jsonify({"reply": "An error occurred while fetching delivery requests. Please try again later."}), 500


def handle_create_delivery(user_context):
    """
    Handle creating a new delivery request.
    """
    return jsonify({"reply": "navigate:create_delivery"}), 200
