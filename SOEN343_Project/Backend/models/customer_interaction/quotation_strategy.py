"""
This module defines the quotation strategy pattern, including the abstract
base class `QuotationStrategy` and its implementations for fragile and standard items.
"""

from abc import ABC, abstractmethod


class QuotationStrategy(ABC):
    """
    QuotationStrategy is an abstract base class that defines the interface
    for calculating a price quotation based on specific strategies.
    """

    @abstractmethod
    def calculate_quote(self, base_price: float) -> float:
        """
        Calculate the price quotation based on the specific strategy.

        Args:
            base_price (float): The base price for the quotation.

        Returns:
            float: The calculated quotation price.
        """
        pass


class FragileQuotationStrategy(QuotationStrategy):
    """
    FragileQuotationStrategy calculates a quotation by adding a surcharge
    for handling fragile items.
    """

    # pylint: disable=too-few-public-methods
    def calculate_quote(self, base_price: float) -> float:
        """
        Calculate the price quotation with a surcharge for fragile items.

        Args:
            base_price (float): The base price for the quotation.

        Returns:
            float: The calculated quotation price with a 20% surcharge.
        """
        return base_price * 1.2


class StandardQuotationStrategy(QuotationStrategy):
    """
    StandardQuotationStrategy calculates a quotation without any surcharges
    for standard items.
    """

    # pylint: disable=too-few-public-methods
    def calculate_quote(self, base_price: float) -> float:
        """
        Calculate the price quotation without any surcharges.

        Args:
            base_price (float): The base price for the quotation.

        Returns:
            float: The calculated quotation price.
        """
        return base_price
