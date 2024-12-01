import pytest
from unittest.mock import MagicMock
from datetime import datetime


def test_make_payment_success(client):
    # Mocking the payment_facade behavior
    mock_payment_facade = MagicMock()
    mock_payment_facade.process_payment_and_create_order.return_value = 101  # Mock order ID
    client.application.config['payment_facade'] = mock_payment_facade

    # Request payload
    payload = {
        "delivery_request_id": 1,
        "payment_method": "mock_payment_token"
    }

    response = client.post('/payment/make_payment', json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "Payment successful and order processed"
    assert data["order_id"] == 101


def test_make_payment_missing_fields(client):
    response = client.post('/payment/make_payment', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Delivery request ID and payment method are required."


def test_make_payment_processing_failed(client):
    mock_payment_facade = MagicMock()
    mock_payment_facade.process_payment_and_create_order.return_value = None  # Simulate failure
    client.application.config['payment_facade'] = mock_payment_facade

    payload = {
        "delivery_request_id": 1,
        "payment_method": "mock_payment_token"
    }

    response = client.post('/payment/make_payment', json=payload)
    data = response.get_json()

    assert response.status_code == 500
    assert data["error"] == "Payment processing failed"


def test_payment_history_success(client):
    mock_payment_facade = MagicMock()
    mock_payment_facade.get_payment_history.return_value = [
        {
            "payment_id": 1,
            "order_id": 101,
            "amount": 50.0,
            "payment_date": datetime.utcnow().isoformat(),
            "status": "Completed"
        }
    ]
    client.application.config['payment_facade'] = mock_payment_facade

    response = client.post('/payment/payment_history', json={"user_id": 1})
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["status"] == "Completed"


def test_payment_history_missing_user_id(client):
    response = client.post('/payment/payment_history', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Customer ID is required."


def test_payment_history_not_found(client):
    mock_payment_facade = MagicMock()
    mock_payment_facade.get_payment_history.return_value = []  # No payments found
    client.application.config['payment_facade'] = mock_payment_facade

    response = client.post('/payment/payment_history', json={"user_id": 1})
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "No payments found for customer ID 1"


def test_payment_status_success(client):
    mock_payment_facade = MagicMock()
    mock_payment_facade.get_payment_status_by_order.return_value = {
        "payment_id": 1,
        "order_id": 101,
        "amount": 50.0,
        "payment_date": datetime.utcnow().isoformat(),
        "status": "Completed"
    }
    client.application.config['payment_facade'] = mock_payment_facade

    response = client.post('/payment/payment_status', json={"order_id": 101})
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "Completed"


def test_payment_status_missing_order_id(client):
    response = client.post('/payment/payment_status', json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Order ID is required."


def test_payment_status_not_found(client):
    mock_payment_facade = MagicMock()
    mock_payment_facade.get_payment_status_by_order.return_value = None  # No payment found
    client.application.config['payment_facade'] = mock_payment_facade

    response = client.post('/payment/payment_status', json={"order_id": 999})
    data = response.get_json()

    assert response.status_code == 404
    assert data["message"] == "No payment found for the given Order ID"
