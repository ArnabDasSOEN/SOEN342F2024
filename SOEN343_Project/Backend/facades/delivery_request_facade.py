
from models.logistics.delivery_request import DeliveryRequest
from services.address_service import AddressService
from services.package_factory import PackageFactory
from services.distance_service import DistanceService
from services.quotation_service import QuotationService
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

        # Step 4: Calculate distance and get quotation price
        distance = DistanceService.calculate(pick_up_address, drop_off_address)
        quotation_price = QuotationService.calculate_quotation(
            delivery_request.id, distance)

        return {
            "delivery_request_id": delivery_request.id,
            "quotation_price": quotation_price
        }
