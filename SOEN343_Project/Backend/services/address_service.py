"""
Address Service Module
Provides functionality for creating or retrieving addresses from the database.
"""

from models.customer_interaction.address import Address
from dbconnection import db


class AddressService:
    """
    Service class for managing address-related database operations.
    """

    @staticmethod
    def create_or_get_address(address_data: dict) -> Address:
        """
        Creates or retrieves an address from the database.

        Args:
            address_data (dict): A dictionary containing address details, including
                                 street, house_number, postal_code, city, and country.

        Returns:
            Address: An instance of the Address model corresponding to the provided data.
        """
        # Query the database to find an address matching the provided details
        address = Address.query.filter_by(
            street=address_data.get("street"),
            house_number=address_data.get("house_number"),
            postal_code=address_data.get("postal_code"),
            city=address_data.get("city"),
            country=address_data.get("country")
        ).first()

        # If no matching address is found, create a new one
        if not address:
            address = Address(**address_data)
            db.session.add(address)
            db.session.commit()

        return address
