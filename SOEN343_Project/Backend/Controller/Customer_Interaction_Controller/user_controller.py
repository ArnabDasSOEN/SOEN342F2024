# controller/user_controller.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.customer_interaction.user import User
from services.user_factory import UserFactory
from dbconnection import db

#from flask import session

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phone_number")
    user_type = data.get("user_type", "customer")  # Default to customer
    admin_id = data.get("admin_id")  # Only required for Admin creation

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    # Validate user_type
    if user_type.lower() in ["admin", "deliveryagent"]:
        # Check if current user is an admin
        current_user_id = data.get("current_user_id")  # Sent in the request
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
            admin_id=admin_id if user_type.lower() == "admin" else None
        )

        return jsonify({"message": f"{user_type} account created successfully!"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

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
