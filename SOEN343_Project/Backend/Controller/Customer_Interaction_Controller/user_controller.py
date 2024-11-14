# controller/user_controller.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.customer_interaction.user import User
from services.user_factory import UserFactory
from dbconnection import db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phone_number")

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Use UserFactory to create a new customer
    customer = UserFactory.create_user(
        user_type="customer",
        name=name,
        password=hashed_password,
        email=email,
        phone_number=phone_number
    )

    return jsonify({"message": "Customer account created successfully!"}), 201


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
        "user_id": user.id
    }), 200
