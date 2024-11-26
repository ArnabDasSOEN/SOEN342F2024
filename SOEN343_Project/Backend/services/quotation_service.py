"""
Quotation Service
Handles the calculation of delivery quotations based on distance, package weight, and additional strategies.
"""

from models.customer_interaction.quotation import Quotation
from models.logistics.delivery_request import DeliveryRequest
from models.customer_interaction.quotation_strategy import FragileQuotationStrategy, StandardQuotationStrategy
from services.distance_service import DistanceService
from dbconnection import db


class QuotationService:
    """
    Service class for calculating and managing delivery quotations.
    """

    @staticmethod
    def calculate_quotation(delivery_request_id: int, pick_up_address, drop_off_address) -> float:
        """
        Calculate the quotation for a delivery request.

        Args:
            delivery_request_id (int): The ID of the delivery request.
            pick_up_address (object): The pickup address object.
            drop_off_address (object): The drop-off address object.

        Returns:
            float: The calculated quotation price.

        Raises:
            ValueError: If the delivery request is not found.
        """
        # Retrieve the delivery request and associated package
        delivery_request = db.session.query(
            DeliveryRequest).get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found.")

        package = delivery_request.package
        is_fragile = package.is_fragile

        # Step 1: Calculate the distance using DistanceService
        pick_up = f"{pick_up_address.street} {pick_up_address.house_number}, {
            pick_up_address.city}, {pick_up_address.country}"
        drop_off = f"{drop_off_address.street} {drop_off_address.house_number}, {
            drop_off_address.city}, {drop_off_address.country}"
        distance = DistanceService.calculate(
            pick_up_address=pick_up, drop_off_address=drop_off)

        # Step 2: Calculate Shipping Weight
        shipping_weight = package.calculate_shipping_weight()

        # Step 3: Define rates
        rate_per_km = 0.5  # Rate per kilometer
        rate_per_kg = 2.0  # Rate per kilogram

        # Step 4: Calculate Base Price
        base_price = (distance * rate_per_km) + (shipping_weight * rate_per_kg)

        # Step 5: Apply Quotation Strategy
        strategy = FragileQuotationStrategy() if is_fragile else StandardQuotationStrategy()
        final_price = strategy.calculate_quote(base_price)

        # Save the calculated quotation in the database
        quotation = Quotation(
            delivery_request_id=delivery_request_id, price=final_price)
        db.session.add(quotation)
        db.session.commit()

        return final_price
