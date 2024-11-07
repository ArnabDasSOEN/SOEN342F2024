# tests/test_user_endpoints.py
def test_create_user(client):
    # Example data for creating a new user
    new_user = {
        "user_type": "admin",
        "name": "John Doe",
        "password": "password123",
        "email": "johndoe@example.com",
        "phone_number": "123-456-7890",
        "admin_id": "A123"
    }

    response = client.post('/user/create_user', json=new_user)
    data = response.get_json()

    # Check that the response is successful
    assert response.status_code == 201
    assert data["message"] == "admin created successfully!"
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]
    assert data["phone_number"] == new_user["phone_number"]
