# Models/Customer_Interaction/user_factory.py
from models.customer_interaction.admin import Admin
from models.customer_interaction.customer import Customer
from models.customer_interaction.delivery_agent import DeliveryAgent
from dbconnection import db


class UserFactory:
    @staticmethod
    def create_user(user_type, name, password, email, phone_number, admin_id=None):
        if user_type.lower() == "admin":
            user = Admin(name, password, email, phone_number, admin_id)
        elif user_type.lower() == "customer":
            user = Customer(name, password, email, phone_number)
        elif user_type.lower() == "deliveryagent":
            user = DeliveryAgent(name, password, email, phone_number)
        else:
            raise ValueError(f"Unknown user type: {user_type}")

        db.session.add(user)
        db.session.commit()  # Save the user to the database
        return user
