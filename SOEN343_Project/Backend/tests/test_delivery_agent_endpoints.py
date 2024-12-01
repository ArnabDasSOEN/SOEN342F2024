import pytest
from .test_utils import create_address, create_package, create_delivery_request
from dbconnection import db
from models.logistics.tracker import Tracker, DeliveryStatus
from models.logistics.order import Order


def create_tracker(order_id, delivery_agent_id, status=DeliveryStatus.IN_TRANSIT.value, estimated_delivery_time=None):
    """
    Create and persist a Tracker object for tests.
    """
    tracker = Tracker(
        order_id=order_id,
        delivery_agent_id=delivery_agent_id,
        status=status,
        estimated_delivery_time=estimated_delivery_time,
    )
    db.session.add(tracker)
    db.session.commit()
    return tracker


# Test: Update Tracker Status

def test_update_status_success(client):
    """Test successfully updating tracker status."""
    with client.application.app_context():
        # Set up test data
        order = Order(delivery_request_id=1, customer_id=1)
        db.session.add(order)
        db.session.commit()

        tracker = create_tracker(order_id=order.id, delivery_agent_id=1)

        # Call the endpoint
        response = client.post(
            "/delivery_agent/update_status",
            json={"tracker_id": tracker.id, "status": "OUT FOR DELIVERY"},
        )
        data = response.get_json()

        # Assertions
        assert response.status_code == 200
        assert data["status"] == "Tracker status updated to OUT FOR DELIVERY"
        db.session.refresh(tracker)
        assert tracker.status == DeliveryStatus.OUT_FOR_DELIVERY.value


def test_update_status_invalid_tracker(client):
    """Test updating status for a non-existent tracker."""
    response = client.post(
        "/delivery_agent/update_status",
        json={"tracker_id": 999, "status": "DELIVERED"},
    )
    data = response.get_json()

    # Assertions
    assert response.status_code == 404
    assert data["error"] == "Tracker not found"


def test_update_status_invalid_status(client):
    """Test updating tracker with an invalid status."""
    with client.application.app_context():
        # Set up test data
        order = Order(delivery_request_id=1, customer_id=1)
        db.session.add(order)
        db.session.commit()

        tracker = create_tracker(order_id=order.id, delivery_agent_id=1)

        # Call the endpoint with an invalid status
        response = client.post(
            "/delivery_agent/update_status",
            json={"tracker_id": tracker.id, "status": "INVALID_STATUS"},
        )
        data = response.get_json()

        # Assertions
        assert response.status_code == 400
        assert data["error"] == "Invalid status provided"


# Test: Track Delivery

def test_track_delivery_success(client):
    """Test successfully retrieving tracker status."""
    with client.application.app_context():
        # Set up test data
        order = Order(delivery_request_id=1, customer_id=1)
        db.session.add(order)
        db.session.commit()

        tracker = create_tracker(
            order_id=order.id, delivery_agent_id=1, status=DeliveryStatus.OUT_FOR_DELIVERY.value, estimated_delivery_time=30
        )

        # Call the endpoint
        response = client.post(
            "/delivery_agent/track",
            json={"order_id": order.id},
        )
        data = response.get_json()

        # Assertions
        assert response.status_code == 200
        assert data["status"] == DeliveryStatus.OUT_FOR_DELIVERY.value
        assert data["estimated_delivery_time"] == 30
        assert data["message"] == "Delivery agent is en route to your destination."


def test_track_delivery_completed(client):
    """Test tracking delivery when the delivery is completed."""
    with client.application.app_context():
        # Set up test data
        order = Order(delivery_request_id=1, customer_id=1)
        db.session.add(order)
        db.session.commit()

        tracker = create_tracker(
            order_id=order.id, delivery_agent_id=1, status=DeliveryStatus.DELIVERED.value
        )

        # Call the endpoint
        response = client.post(
            "/delivery_agent/track",
            json={"order_id": order.id},
        )
        data = response.get_json()

        # Assertions
        assert response.status_code == 200
        assert data["status"] == DeliveryStatus.DELIVERED.value
        assert data["message"] == "The delivery has been successfully completed."


def test_track_delivery_missing_order_id(client):
    """Test tracking delivery with missing order ID."""
    response = client.post(
        "/delivery_agent/track",
        json={},
    )
    data = response.get_json()

    # Assertions
    assert response.status_code == 400
    assert data["error"] == "Order ID is required"


def test_track_delivery_not_found(client):
    """Test tracking delivery for a non-existent order."""
    response = client.post(
        "/delivery_agent/track",
        json={"order_id": 999},
    )
    data = response.get_json()

    # Assertions
    assert response.status_code == 404
    assert data["error"] == "Tracker not found for the given Order ID"
