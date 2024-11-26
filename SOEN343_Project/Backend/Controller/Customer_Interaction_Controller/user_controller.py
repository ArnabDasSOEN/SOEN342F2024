"""
This module defines routes for user authentication, including user sign-up
and login functionality. It interacts with the User model and UserFactory service.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.customer_interaction.user import User
from services.user_factory import UserFactory

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    """
    Create a new user account.

    Expects JSON data:
    {
        "name": <str>,
        "password": <str>,
        "email": <str>,
        "phone_number": <str>,
        "user_type": <str>,  # Optional, defaults to "customer"
        "admin_id": <str>,  # Required for Admin accounts
        "current_user_id": <int>  # Required for creating Admin or DeliveryAgent accounts
    }

    Returns:
        - 201: Account created successfully.
        - 400: Email already registered or validation error.
        - 403: Unauthorized to create Admin or DeliveryAgent accounts.
        - 500: Unexpected server error.
    """
    data = request.json
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phone_number")
    # Default to customer
    user_type = data.get("user_type", "customer").lower()
    admin_id = data.get("admin_id")

    if not all([name, password, email, phone_number]):
        return jsonify({"error": "All fields except 'admin_id' are required."}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    # Validate user_type for special accounts
    if user_type in ["admin", "deliveryagent"]:
        current_user_id = data.get("current_user_id")
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.type.lower() != "admin":
            return jsonify({"error": "Only admins can create Admin or DeliveryAgent accounts."}), 403

    # Hash the password for security
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        # Use UserFactory to create a new user
        user = UserFactory.create_user(
            user_type=user_type,
            name=name,
            password=hashed_password,
            email=email,
            phone_number=phone_number,
            admin_id=admin_id if user_type == "admin" else None
        )
        return jsonify({"message": f"{user_type.capitalize()} account created successfully!"}), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": f"Server error: {error}"}), 500


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Log in a user.

    Expects JSON data:
    {
        "email": <str>,
        "password": <str>
    }

    Returns:
        - 200: Login successful.
        - 404: User not found.
        - 401: Incorrect password.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Check password
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password."}), 401

    return jsonify({
        "message": "Login successful!",
        "user_type": user.type,
        "user_id": user.id,
        "username": user.name
    }), 200
