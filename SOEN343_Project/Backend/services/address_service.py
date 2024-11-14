from models.customer_interaction.address import Address
from dbconnection import db


class AddressService:
    @staticmethod
    def create_or_get_address(address_data: dict) -> Address:
        address = Address.query.filter_by(
            street=address_data["street"],
            house_number=address_data["house_number"],
            postal_code=address_data["postal_code"],
            city=address_data["city"],
            country=address_data["country"]
        ).first()

        if not address:
            address = Address(**address_data)
            db.session.add(address)
            db.session.commit()

        return address
