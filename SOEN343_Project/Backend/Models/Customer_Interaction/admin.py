"""
This module defines the Admin class, which extends the User class
to include additional functionality and attributes specific to administrators.
"""

from dbconnection import db
from .user import User


class Admin(User):
    """
    The Admin class represents administrators in the system, inheriting
    common user attributes and functionality while adding admin-specific features.
    """
    __tablename__ = 'admins'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # Specific field for Admin
    admin_id = db.Column(db.String(20), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, **kwargs):
        """
        Initialize an Admin instance using keyword arguments.

        Args:
            kwargs (dict): Dictionary containing admin attributes.
        """
        super().__init__(
            name=kwargs.get('name'),
            password=kwargs.get('password'),
            email=kwargs.get('email'),
            phone_number=kwargs.get('phone_number')
        )
        self.admin_id = kwargs.get('admin_id')
