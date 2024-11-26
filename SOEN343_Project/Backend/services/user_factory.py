"""
User Factory
Handles the creation of users of different types (Admin, Customer, DeliveryAgent).
"""

from models.customer_interaction.admin import Admin
from models.customer_interaction.customer import Customer
from models.customer_interaction.delivery_agent import DeliveryAgent
from dbconnection import db


class UserFactory:
    """
    A factory class for creating users of different types.
    """

    @staticmethod
    def create_user(user_type: str, name: str, password: str, email: str, phone_number: str, admin_id: int = None):
        """
        Creates a user based on the specified user type.

        Args:
            user_type (str): The type of user to create ('admin', 'customer', or 'deliveryagent').
            name (str): The name of the user.
            password (str): The user's password.
            email (str): The user's email address.
            phone_number (str): The user's phone number.
            admin_id (int, optional): The ID of the admin creating the user (required for 'admin' user type).

        Returns:
            Union[Admin, Customer, DeliveryAgent]: The created user instance.

        Raises:
            ValueError: If an unknown user type is specified or if `admin_id` is missing for admin creation.
        """
        user_type = user_type.lower()

        if user_type == "admin":
            if not admin_id:
                raise ValueError("Admin creation requires an admin_id.")
            user = Admin(name=name, password=password, email=email,
                         phone_number=phone_number, admin_id=admin_id)
        elif user_type == "customer":
            user = Customer(name=name, password=password,
                            email=email, phone_number=phone_number)
        elif user_type == "deliveryagent":
            user = DeliveryAgent(name=name, password=password,
                                 email=email, phone_number=phone_number)
        else:
            raise ValueError(f"Unknown user type: {user_type}")

        db.session.add(user)
        db.session.commit()
        return user
