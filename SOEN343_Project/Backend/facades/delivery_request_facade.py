from models.logistics.delivery_request import DeliveryRequest
from services.address_service import AddressService
from services.package_factory import PackageFactory
from services.quotation_service import QuotationService
from services.package_update_service import PackageUpdateService
from dbconnection import db


class DeliveryRequestFacade:
    def create_delivery_request_with_quotation(self, customer_id: int, pick_up_address_data: dict, drop_off_address_data: dict, package_data: dict) -> dict:
        # Step 1: Create or retrieve addresses
        pick_up_address = AddressService.create_or_get_address(
            pick_up_address_data)
        drop_off_address = AddressService.create_or_get_address(
            drop_off_address_data)

        # Step 2: Create the package
        package = PackageFactory.create_package(package_data)

        # Step 3: Create and save the delivery request
        delivery_request = DeliveryRequest(
            customer_id=customer_id,
            package_id=package.id,
            pick_up_address_id=pick_up_address.id,
            drop_off_address_id=drop_off_address.id
        )
        db.session.add(delivery_request)
        db.session.commit()

        # Step 4: Calculate quotation price using QuotationService
        quotation_price = QuotationService.calculate_quotation(
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
        # Retrieve the delivery request
        delivery_request = DeliveryRequest.query.get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found")

        # Check if the delivery request can be updated
        if delivery_request.status.lower() in ["paid", "cancelled", "delivered"]:
            raise ValueError(f"Cannot update delivery request in '{
                             delivery_request.status}' state")

        # Step 1: Update or retrieve addresses if provided
        pick_up_address = None
        drop_off_address = None

        if pick_up_address_data:
            pick_up_address = AddressService.create_or_get_address(
                pick_up_address_data)
            delivery_request.pick_up_address_id = pick_up_address.id

        if drop_off_address_data:
            drop_off_address = AddressService.create_or_get_address(
                drop_off_address_data)
            delivery_request.drop_off_address_id = drop_off_address.id

        # Step 2: Update the package if provided
        if package_data:
            updated_package = PackageUpdateService.update_package(
                delivery_request.package_id, package_data
            )
            delivery_request.package_id = updated_package.id

        # Commit changes to the delivery request
        db.session.commit()

        # Step 3: Recalculate quotation
        new_quotation_price = QuotationService.calculate_quotation(
            delivery_request_id=delivery_request.id,
            pick_up_address=pick_up_address or delivery_request.pick_up_address,
            drop_off_address=drop_off_address or delivery_request.drop_off_address
        )

        return {
            "message": "Delivery request updated successfully",
            "delivery_request_id": delivery_request.id,
            "new_quotation_price": new_quotation_price
        }
