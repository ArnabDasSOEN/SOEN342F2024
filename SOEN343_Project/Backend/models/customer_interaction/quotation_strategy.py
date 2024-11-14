from abc import ABC, abstractmethod


class QuotationStrategy(ABC):
    @abstractmethod
    def calculate_quote(self, base_price: float) -> float:
        pass


class FragileQuotationStrategy(QuotationStrategy):
    def calculate_quote(self, base_price: float) -> float:
        # Add an extra charge for fragile items, e.g., 20%
        return base_price * 1.2


class StandardQuotationStrategy(QuotationStrategy):
    def calculate_quote(self, base_price: float) -> float:
        # Standard calculation without extra charges
        return base_price
