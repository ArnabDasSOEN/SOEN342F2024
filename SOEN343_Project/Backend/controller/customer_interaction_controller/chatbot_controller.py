# chatbot_controller.py
from flask import Blueprint, request, jsonify
import openai
from extensions import limiter  # Import limiter from extensions
from models.logistics.delivery_request import DeliveryRequest
from models.logistics.order import Order
from models.logistics.payment import Payment
import requests
import os

chatbot_blueprint = Blueprint('chatbot', __name__, url_prefix='/chatbot')


@chatbot_blueprint.route('/ask', methods=['POST'])
@limiter.limit("3 per minute")  # Apply rate limiting
def ask_chatbot():
    """
    Handle user queries via chatbot.
    """
    data = request.json
    user_message = data.get("message")
    user_context = data.get("context", {})  # Optional user-specific data

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Task-specific commands
        if "track my delivery" in user_message.lower():
            return handle_track_delivery(user_context)
        elif "view my payment history" in user_message.lower():
            return handle_view_payment_history(user_context)
        elif "check payment status" in user_message.lower():
            return handle_payment_status(user_context)
        elif "update my delivery" in user_message.lower():
            return handle_update_delivery_request(user_context)
        elif "create delivery request" in user_message.lower():
            return handle_create_delivery_request(user_context)
        elif "cancel my delivery" in user_message.lower():
            return handle_cancel_delivery_request(user_context)
        elif "view my delivery requests" in user_message.lower():
            return handle_view_delivery_requests(user_context)

        # Default fallback to GPT for general queries
        openai_api_key = os.getenv("OPEN_AI_API_KEY")
        if not openai_api_key:
            return jsonify({"error": "OpenAI API key not configured in environment variables"}), 500

        openai.api_key = openai_api_key  # Set the API key
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a delivery service. You assist with:\n"
                 "1. Requesting a delivery.\n"
                 "2. Proposing a quotation.\n"
                 "3. Answering communication inquiries.\n"
                 "4. Tracking an order (requires an order ID).\n"
                 "5. Handling payment-related inquiries.\n"
                 "6. Providing help and guidance within the delivery service domain.\n"
                 "If the user asks for tracking, payment, or updating a delivery, ensure they provide necessary IDs or data."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=100
        )

        chatbot_reply = response.choices[0].message.content
        return jsonify({"reply": chatbot_reply}), 200

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Task-specific handlers


def handle_track_delivery(user_context):
    """
    Handle tracking delivery requests.
    """
    order_id = user_context.get("order_id")
    if not order_id:
        return jsonify({"reply": "Please provide your order ID to track your delivery."}), 200

    # Call the tracking endpoint
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


def handle_view_payment_history(user_context):
    """
    Handle viewing payment history and prompt for payment ID to check its status.
    """
    user_id = user_context.get("user_id")  # Validate user login
    if not user_id:
        return jsonify({"reply": "User ID is missing in the context. Please log in again."}), 401

    # Fetch payment history
    response = requests.post(
        f"{request.host_url}payment/payment_history",
        json={"user_id": user_id}
    )
    if response.status_code == 200:
        payments = response.json()
        if not payments:
            return jsonify({"reply": "You have no payments in your history."}), 200

        # Display payments and prompt for an action
        reply = "Here are your payments:\n"
        for payment in payments:
            reply += f"- Payment ID: {payment['payment_id']}, Amount: {
                payment['amount']}, Status: {payment['status']}, Order ID: {payment['order_id']}\n"
        reply += "Please reply with the Order ID to check its status."
        return jsonify({"reply": reply}), 200
    else:
        return jsonify({"reply": "Failed to fetch payment history. Please try again later."}), 500


def handle_payment_status(user_context):
    """
    Handle checking payment status after prompting for a valid Order ID.
    """
    order_id = user_context.get("order_id")
    if not order_id:
        return jsonify({"reply": "Please provide a valid Order ID from your payment history to check its status."}), 200

    # Fetch payment status
    response = requests.post(
        f"{request.host_url}payment/payment_status",
        json={"order_id": order_id}
    )
    if response.status_code == 200:
        payment_status = response.json()
        return jsonify({"reply": f"Payment Status: {payment_status['status']}, Amount: {payment_status['amount']}."}), 200
    else:
        return jsonify({"reply": "Failed to fetch payment status. Please ensure the Payment ID is correct."}), 500


def handle_cancel_delivery_request(user_context):
    """
    Display delivery requests for the logged-in user and prompt for ID to cancel.
    """
    user_id = user_context.get("user_id")
    if not user_id:
        return jsonify({"reply": "User ID is missing in the context. Please log in again."}), 401

    # Fetch user's delivery requests
    response = requests.post(
        f"{request.host_url}delivery_request/view_delivery_requests",
        json={"user_id": user_id}
    )
    if response.status_code == 200:
        delivery_requests = response.json()
        if not delivery_requests:
            return jsonify({"reply": "You have no delivery requests to cancel."}), 200

        # Display requests and prompt for an action
        reply = "Here are your delivery requests:\n"
        for req in delivery_requests:
            reply += f"- Request ID: {req['delivery_request_id']
                                      }, Status: {req['status']}\n"
        reply += "Reply with the Delivery Request ID you want to cancel."
        return jsonify({"reply": reply}), 200
    else:
        return jsonify({"reply": "Failed to fetch delivery requests. Please try again later."}), 500


def handle_update_delivery_request(user_context):
    """
    Display delivery requests for the logged-in user and prompt for ID to update.
    """
    user_id = user_context.get("user_id")
    if not user_id:
        return jsonify({"reply": "User ID is missing in the context. Please log in again."}), 401

    # Fetch user's delivery requests
    response = requests.post(
        f"{request.host_url}delivery_request/view_delivery_requests",
        json={"user_id": user_id}
    )
    if response.status_code == 200:
        delivery_requests = response.json()
        if not delivery_requests:
            return jsonify({"reply": "You have no delivery requests to update."}), 200

        # Display requests and prompt for an action
        reply = "Here are your delivery requests:\n"
        for req in delivery_requests:
            reply += f"- Request ID: {req['delivery_request_id']
                                      }, Status: {req['status']}\n"
        reply += "Reply with the Delivery Request ID you want to update and provide the update details."
        return jsonify({"reply": reply}), 200
    else:
        return jsonify({"reply": "Failed to fetch delivery requests. Please try again later."}), 500


def handle_create_delivery_request(user_context):
    """
    Handle creating a delivery request.
    """
    data = user_context.get("delivery_request_data")
    if not data:
        return jsonify({"reply": "Please provide the delivery request details."}), 200

    # Call the create delivery request endpoint
    response = requests.post(
        f"{request.host_url}delivery_request/create_delivery_request",
        json=data
    )
    if response.status_code == 201:
        creation_response = response.json()
        return jsonify({"reply": f"Delivery request created successfully. {creation_response}"}), 201
    else:
        return jsonify({"reply": "Failed to create delivery request. Please check your inputs."}), 500


def handle_view_delivery_requests(user_context):
    """
    Handle viewing delivery requests for the logged-in user.
    """
    user_id = user_context.get("user_id")
    if not user_id:
        return jsonify({"reply": "User ID is missing in the context. Please log in again."}), 401

    # Fetch delivery requests
    response = requests.post(
        f"{request.host_url}delivery_request/view_delivery_requests",
        json={"user_id": user_id}
    )
    if response.status_code == 200:
        delivery_requests = response.json()
        reply = "Here are your delivery requests:\n"
        for request in delivery_requests:
            reply += f"- Request ID: {request['delivery_request_id']
                                      }, Status: {request['status']}\n"
        reply += "Reply with the Request ID to perform actions (e.g., cancel, update)."
        return jsonify({"reply": reply}), 200
    else:
        return jsonify({"reply": "Failed to fetch delivery requests."}), 500
