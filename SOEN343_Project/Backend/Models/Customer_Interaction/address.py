"""
This module defines the Address class, which represents an address associated
with a customer or order in the system.
"""

from dbconnection import db


class Address(db.Model):
    """
    Address represents a physical address, including street, house number, apartment number,
    postal code, city, and country.
    """
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.String(10), nullable=False)
    apartment_number = db.Column(db.String(10), nullable=True)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize an Address instance using keyword arguments.

        Args:
            kwargs (dict): Dictionary of address attributes.
        """
        self.street = kwargs.get('street')
        self.house_number = kwargs.get('house_number')
        self.apartment_number = kwargs.get('apartment_number')
        self.postal_code = kwargs.get('postal_code')
        self.city = kwargs.get('city')
        self.country = kwargs.get('country')
