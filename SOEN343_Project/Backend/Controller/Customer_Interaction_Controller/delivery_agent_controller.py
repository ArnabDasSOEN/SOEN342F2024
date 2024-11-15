from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Models.Customer_Interaction import delivery_agent
from services import user_factory
from dbconnection import db

delivery_agent_auth_blueprint = Blueprint('delivery_agent_auth', __name__, url_prefix='/delivery_agent_auth')

@delivery_agent_auth_blueprint.route('/sign_up', methods=['POST'])
def delivery_agent_signup():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phone_number")

    # Check if delivery agent already exists
    if delivery_agent.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Use UserFactory to create a new delivery agent
    customer = user_factory.create_user(
        user_type="delivery_agent",
        name=name,
        password=hashed_password,
        email=email,
        phone_number=phone_number
    )

    return jsonify({"message": "Delivery agent account created successfully!"}), 201

@delivery_agent_auth_blueprint.route('/login', methods=['POST'])
def delivery_agent_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Find user by email
    user = delivery_agent.query.filter_by(email=email).first()
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