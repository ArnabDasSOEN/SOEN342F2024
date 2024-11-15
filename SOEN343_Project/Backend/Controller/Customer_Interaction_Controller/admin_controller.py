from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Models.Customer_Interaction import admin
from services import user_factory
from dbconnection import db

admin_auth_blueprint = Blueprint('admin_auth', __name__, url_prefix='/admin_auth')

@admin_auth_blueprint.route('/sign_up', methods=['POST'])
def admin_signup():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phone_number")
    admin_id = data.get("admin_id")

    # Check if admin already exists
    if admin.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Use UserFactory to create a new admin
    customer = user_factory.create_user(
        user_type="admin",
        name=name,
        password=hashed_password,
        email=email,
        phone_number=phone_number,
        admin_id=admin_id
    )

    return jsonify({"message": "Admin account created successfully!"}), 201

@admin_auth_blueprint.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Find user by email
    user = admin.query.filter_by(email=email).first()
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
