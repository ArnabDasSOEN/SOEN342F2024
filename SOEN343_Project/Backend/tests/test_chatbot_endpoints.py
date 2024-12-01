import pytest
from unittest.mock import patch


def test_ask_chatbot_track_delivery(client):
    user_message = "track my delivery"
    user_context = {"user_id": "123"}

    response = client.post(
        '/chatbot/ask', json={"message": user_message, "context": user_context})
    data = response.get_json()

    assert response.status_code == 200
    assert "Please provide your order ID to track your delivery." in data["reply"]


@patch('requests.post')
def test_ask_chatbot_check_payment_status(mock_post, client):
    # Mock the external API response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "status": "Paid", "amount": "50.00"
    }

    user_id = "123"

    # Step 1: Send the initial command
    response = client.post(
        '/chatbot/ask', json={"message": "check payment status", "context": {"user_id": user_id}}
    )
    data = response.get_json()

    # Check if chatbot sets pending command for "check_payment_status"
    assert response.status_code == 200
    assert "Please provide your order ID to check payment status." in data["reply"]

    # Step 2: Send the follow-up message with order ID
    response = client.post(
        '/chatbot/ask', json={"message": "12345", "context": {"user_id": user_id}}
    )
    data = response.get_json()

    # Check if chatbot resolves "check_payment_status" correctly
    assert response.status_code == 200
    assert "Payment Status: Paid, Amount: 50.00." in data["reply"]

    # Verify the mocked API call
    mock_post.assert_called_with(
        # Ensure the correct endpoint is called
        'http://localhost/payment/payment_status',
        json={"order_id": "12345"}  # Ensure the correct payload is sent
    )


def test_ask_chatbot_missing_message(client):
    response = client.post(
        '/chatbot/ask', json={"context": {"user_id": "123"}})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Message is required"


def test_ask_chatbot_missing_user_id(client):
    response = client.post(
        '/chatbot/ask', json={"message": "track my delivery", "context": {}})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "User ID is required in context"
