from models.customer_interaction.quotation import Quotation
from models.logistics.delivery_request import DeliveryRequest
from models.customer_interaction.quotation_strategy import FragileQuotationStrategy, StandardQuotationStrategy
from services.distance_service import DistanceService
from dbconnection import db


class QuotationService:
    @staticmethod
    def calculate_quotation(delivery_request_id: int, pick_up_address, drop_off_address) -> float:
        """
        Calculate the quotation for a delivery request using distance and package metrics.

        :param delivery_request_id: The ID of the delivery request.
        :param pick_up_address: The pickup address object.
        :param drop_off_address: The drop-off address object.
        :return: The calculated quotation price.
        """
        # Retrieve the delivery request and associated package
        delivery_request = db.session.query(DeliveryRequest).get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found.")

        package = delivery_request.package
        is_fragile = package.is_fragile

        # Step 1: Calculate the distance using DistanceService
        distance = DistanceService.calculate(
            pick_up_address=f"{pick_up_address.street} {pick_up_address.house_number}, {pick_up_address.city}, {pick_up_address.country}",
            drop_off_address=f"{drop_off_address.street} {drop_off_address.house_number}, {drop_off_address.city}, {drop_off_address.country}"
        )

        # Step 2: Calculate Shipping Weight
        shipping_weight = package.calculate_shipping_weight()

        # Step 3: Define rate per kilometer and rate per kilogram
        rate_per_km = 0.5  # Example rate per kilometer
        rate_per_kg = 2.0  # Example rate per kilogram

        # Step 4: Calculate Base Price
        base_price = (distance * rate_per_km) + (shipping_weight * rate_per_kg)

        # Step 5: Apply Strategy to Adjust Price
        strategy = FragileQuotationStrategy() if is_fragile else StandardQuotationStrategy()
        final_price = strategy.calculate_quote(base_price)

        # Save the calculated quotation in the database
        quotation = Quotation(delivery_request_id=delivery_request_id, price=final_price)
        db.session.add(quotation)
        db.session.commit()

        return final_price
