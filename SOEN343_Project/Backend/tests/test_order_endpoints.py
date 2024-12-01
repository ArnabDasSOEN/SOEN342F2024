from .test_utils import create_address, create_package, create_delivery_request
from models.logistics.order import Order
from dbconnection import db


def test_get_orders_by_user_success(client):
    """Test retrieving orders by a valid user."""
    with client.application.app_context():
        # Set up test data
        pick_up_address = create_address(street="123 Main St", city="City A")
        drop_off_address = create_address(street="456 Elm St", city="City B")
        package = create_package()
        delivery_request = create_delivery_request(
            pick_up_address_id=pick_up_address.id,
            drop_off_address_id=drop_off_address.id,
            package_id=package.id,
        )

        # Create an order linked to the delivery request
        order = Order(
            delivery_request_id=delivery_request.id,
            status="Pending",
            customer_id=1,  # Test user ID
        )
        db.session.add(order)
        db.session.commit()

        # Make the API call
        response = client.post(
            "/order/get_orders_by_user", json={"user_id": 1}
        )
        data = response.get_json()

        # Assertions
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["order_id"] == order.id
        assert data[0]["delivery_request"]["pick_up_address"]["street"] == "123 Main St"
        assert data[0]["delivery_request"]["drop_off_address"]["street"] == "456 Elm St"


def test_get_orders_by_user_no_orders(client):
    """Test retrieving orders when the user has no orders."""
    response = client.post(
        "/order/get_orders_by_user", json={"user_id": 2}  # User with no orders
    )
    data = response.get_json()

    # Assertions
    assert response.status_code == 404
    assert data["message"] == "No orders found for user_id 2"


def test_get_orders_by_user_invalid_user_id(client):
    """Test retrieving orders with an invalid user_id."""
    response = client.post(
        "/order/get_orders_by_user", json={"user_id": "invalid_id"}
    )
    data = response.get_json()

    # Assertions
    assert response.status_code == 400
    assert data["error"] == "user_id is required and must be an integer"


def test_get_orders_by_user_missing_user_id(client):
    """Test retrieving orders with missing user_id."""
    response = client.post(
        "/order/get_orders_by_user", json={}
    )
    data = response.get_json()

    # Assertions
    assert response.status_code == 400
    assert data["error"] == "Invalid JSON payload"
