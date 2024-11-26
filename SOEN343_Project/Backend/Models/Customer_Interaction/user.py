"""
This module defines the User class, which represents a user in the system.
The class is designed for use with SQLAlchemy for database interactions.
"""

from dbconnection import db


class User(db.Model):
    """
    The User class represents a user in the system. It includes fields for user details,
    and is designed for polymorphic use in SQLAlchemy with different user types.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    type = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user',
        'with_polymorphic': '*'
    }

    # pylint: disable=too-few-public-methods
    def __init__(self, name: str, password: str, email: str, phone_number: str = None):
        """
        Initialize a User instance.

        Args:
            name (str): The name of the user.
            password (str): The user's password.
            email (str): The user's email address.
            phone_number (str, optional): The user's phone number.
        """
        self.name = name
        self.password = password
        self.email = email
        self.phone_number = phone_number
