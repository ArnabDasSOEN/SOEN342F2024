"""
This module defines the StandardPackageSpecification class, which represents
the dimensions and weight of a standard package.
"""

from dbconnection import db


class StandardPackageSpecification(db.Model):
    """
    StandardPackageSpecification represents the specifications of a standard package,
    including its dimensions (width, length, height) and weight.
    """

    __tablename__ = 'standard_package_specifications'

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Float, nullable=False)
    length = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __init__(self, width: float, length: float, height: float, weight: float):
        """
        Initialize a StandardPackageSpecification instance.

        Args:
            width (float): The width of the package in appropriate units.
            length (float): The length of the package in appropriate units.
            height (float): The height of the package in appropriate units.
            weight (float): The weight of the package in appropriate units.
        """
        self.width = width
        self.length = length
        self.height = height
        self.weight = weight

    def get_weight(self) -> float:
        """
        Retrieve the base weight of the package.

        Returns:
            float: The weight of the package.
        """
        return self.weight

    def get_dimensions(self) -> list:
        """
        Retrieve the dimensions of the package as a list.

        Returns:
            list: A list containing the width, length, and height of the package.
        """
        return [self.width, self.length, self.height]
