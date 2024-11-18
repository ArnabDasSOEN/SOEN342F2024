# chatbot_controller.py
from flask import Blueprint, request, jsonify
import openai
from extensions import limiter  # Import limiter from extensions
from models.logistics.delivery_request import DeliveryRequest
from models.logistics.order import Order
from models.logistics.payment import Payment
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
        # Retrieve OpenAI API key
        openai_api_key = os.getenv("OPEN_AI_API_KEY")
        if not openai_api_key:
            return jsonify({"error": "OpenAI API key not configured in environment variables"}), 500

        openai.api_key = openai_api_key  # Set the API key

        # Generate GPT response
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a delivery service."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=100  # Reduce tokens to stay within quota
        )

        # Extract chatbot response
        chatbot_reply = response.choices[0].message.content
        return jsonify({"reply": chatbot_reply}), 200

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
