from models.logistics.delivery_request import DeliveryRequest
from services.address_service import AddressService
from services.package_factory import PackageFactory
from services.quotation_service import QuotationService
from services.package_update_service import PackageUpdateService
from dbconnection import db


class DeliveryRequestFacade:
    def create_delivery_request_with_quotation(self, customer_id: int, pick_up_address_data: dict, drop_off_address_data: dict, package_data: dict) -> dict:
        # Create or retrieve addresses
        pick_up_address = self._create_or_get_address(pick_up_address_data)
        drop_off_address = self._create_or_get_address(drop_off_address_data)

        # Create the package
        package = PackageFactory.create_package(package_data)

        # Create and save the delivery request
        delivery_request = self._save_delivery_request(
            customer_id=customer_id,
            package_id=package.id,
            pick_up_address_id=pick_up_address.id,
            drop_off_address_id=drop_off_address.id
        )

        # Calculate quotation
        quotation_price = self._calculate_quotation(
            delivery_request_id=delivery_request.id,
            pick_up_address=pick_up_address,
            drop_off_address=drop_off_address
        )

        return {
            "delivery_request_id": delivery_request.id,
            "quotation_price": quotation_price
        }

    def update_delivery_request(
        self, delivery_request_id: int, pick_up_address_data: dict = None,
        drop_off_address_data: dict = None, package_data: dict = None
    ) -> dict:
        delivery_request = self._get_and_validate_delivery_request(
            delivery_request_id)

        # Update addresses if provided
        if pick_up_address_data:
            pick_up_address = self._create_or_get_address(pick_up_address_data)
            delivery_request.pick_up_address_id = pick_up_address.id

        if drop_off_address_data:
            drop_off_address = self._create_or_get_address(
                drop_off_address_data)
            delivery_request.drop_off_address_id = drop_off_address.id

        # Update the package if provided
        if package_data:
            updated_package = self._update_package(
                delivery_request.package_id, package_data)
            delivery_request.package_id = updated_package.id

        # Commit changes
        db.session.commit()

        # Recalculate quotation
        new_quotation_price = self._calculate_quotation(
            delivery_request_id=delivery_request.id,
            pick_up_address=pick_up_address or delivery_request.pick_up_address,
            drop_off_address=drop_off_address or delivery_request.drop_off_address
        )

        return {
            "message": "Delivery request updated successfully",
            "delivery_request_id": delivery_request.id,
            "new_quotation_price": new_quotation_price
        }

    # Helper methods
    def _create_or_get_address(self, address_data: dict):
        """Create or retrieve an address."""
        return AddressService.create_or_get_address(address_data)

    def _save_delivery_request(self, customer_id: int, package_id: int, pick_up_address_id: int, drop_off_address_id: int) -> DeliveryRequest:
        """Save a delivery request to the database."""
        delivery_request = DeliveryRequest(
            customer_id=customer_id,
            package_id=package_id,
            pick_up_address_id=pick_up_address_id,
            drop_off_address_id=drop_off_address_id
        )
        db.session.add(delivery_request)
        db.session.commit()
        return delivery_request

    def _calculate_quotation(self, delivery_request_id: int, pick_up_address, drop_off_address) -> float:
        """Calculate the quotation price."""
        return QuotationService.calculate_quotation(
            delivery_request_id=delivery_request_id,
            pick_up_address=pick_up_address,
            drop_off_address=drop_off_address
        )

    def _update_package(self, package_id: int, package_data: dict):
        """Update a package with new data."""
        return PackageUpdateService.update_package(package_id, package_data)

    def _get_and_validate_delivery_request(self, delivery_request_id: int) -> DeliveryRequest:
        """Retrieve and validate a delivery request."""
        delivery_request = DeliveryRequest.query.get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found")

        if delivery_request.status.lower() in ["paid", "cancelled", "delivered"]:
            raise ValueError(
                f"Cannot update delivery request in '{
                    delivery_request.status}' state"
            )
        return delivery_request
