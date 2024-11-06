import requests

url = "http://127.0.0.1:5000/add_user"
user_data = {
    "username": "john_doe",
    "password": "password123",
    "phoneNumber": "1234567890",
    "email": "john@example.com"
}

response = requests.post(url, json=user_data)

print(response.status_code)
print(response.json())