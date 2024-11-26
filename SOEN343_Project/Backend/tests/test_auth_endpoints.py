# tests/test_user_endpoints.py
def test_sign_up_success(client):
    new_user = {
        "name": "John Doe",
        "password": "password123",
        "email": "johndoe@example.com",
        "phone_number": "123-456-7890",
        "user_type": "customer"
    }
    response = client.post('/auth/sign_up', json=new_user)
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Customer account created successfully!"


def test_sign_up_missing_fields(client):
    incomplete_user = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }
    response = client.post('/auth/sign_up', json=incomplete_user)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "All fields except 'admin_id' are required."


def test_sign_up_existing_email(client):
    existing_user = {
        "name": "John Doe",
        "password": "password123",
        "email": "johndoe@example.com",
        "phone_number": "123-456-7890",
        "user_type": "customer"
    }
    client.post('/auth/sign_up', json=existing_user)  # Create the user first

    response = client.post('/auth/sign_up', json=existing_user)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Email already registered."


def test_sign_up_admin_requires_admin(client):
    # Create a non-admin user
    client.post('/auth/sign_up', json={
        "name": "User",
        "password": "password123",
        "email": "user@example.com",
        "phone_number": "123-456-7890",
        "user_type": "customer"
    })

    new_admin = {
        "name": "Admin User",
        "password": "password123",
        "email": "admin@example.com",
        "phone_number": "123-456-7890",
        "user_type": "admin",
        "current_user_id": 1  # Non-admin user ID
    }
    response = client.post('/auth/sign_up', json=new_admin)
    data = response.get_json()

    assert response.status_code == 403
    assert data["error"] == "Only admins can create Admin or DeliveryAgent accounts."


def test_login_success(client):
    user = {
        "name": "John Doe",
        "password": "password123",
        "email": "johndoe@example.com",
        "phone_number": "123-456-7890",
        "user_type": "customer"
    }
    client.post('/auth/sign_up', json=user)  # Create the user first

    response = client.post('/auth/login', json={
        "email": "johndoe@example.com",
        "password": "password123"
    })
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Login successful!"
    assert data["user_type"] == "customer"
    assert data["username"] == "John Doe"


def test_login_incorrect_password(client):
    user = {
        "name": "John Doe",
        "password": "password123",
        "email": "johndoe@example.com",
        "phone_number": "123-456-7890",
        "user_type": "customer"
    }
    client.post('/auth/sign_up', json=user)  # Create the user first

    response = client.post('/auth/login', json={
        "email": "johndoe@example.com",
        "password": "wrongpassword"
    })
    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Incorrect password."


def test_login_user_not_found(client):
    response = client.post('/auth/login', json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "User not found."
