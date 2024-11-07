# Controller/user_controller.py
from flask import Blueprint, request, jsonify
from Models.Customer_Interaction.user_factory import UserFactory
from Models.Customer_Interaction.user import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user_type = data.get("user_type")
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phone_number")
    admin_id = data.get("admin_id", None)  # Only for Admin users

    try:
        user = UserFactory.create_user(user_type, name, password, email, phone_number, admin_id)
        return jsonify({
            "message": f"{user_type} created successfully!",
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{"name": u.name, "email": u.email, "phone_number": u.phone_number, "type": u.type} for u in users]
    return jsonify(users_data), 200
