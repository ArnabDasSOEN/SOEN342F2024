from models.customer_interaction.quotation import Quotation
from models.logistics.delivery_request import DeliveryRequest
from models.customer_interaction.quotation_strategy import FragileQuotationStrategy, StandardQuotationStrategy
from dbconnection import db


class QuotationService:
    @staticmethod
    def calculate_quotation(delivery_request_id: int, distance: float) -> float:
        # Retrieve the delivery request and associated package
        delivery_request = db.session.query(
            DeliveryRequest).get(delivery_request_id)
        if not delivery_request:
            raise ValueError("Delivery request not found")

        package = delivery_request.package
        is_fragile = package.is_fragile
        strategy = FragileQuotationStrategy() if is_fragile else StandardQuotationStrategy()

        # Define rate per km (could be a config setting)
        rate_per_km = 0.5
        base_price = distance * rate_per_km

        # Calculate the final price using the selected strategy
        final_price = strategy.calculate_quote(base_price)

        # Save the calculated quotation
        quotation = Quotation(
            delivery_request_id=delivery_request_id, price=final_price)
        db.session.add(quotation)
        db.session.commit()

        return final_price
