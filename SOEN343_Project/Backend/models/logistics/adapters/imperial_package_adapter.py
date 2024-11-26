"""
This module provides the ImperialPackageAdapter class, which adapts imperial package
specifications to standard metric specifications for use in the system.
"""

from models.customer_interaction.standard_package_specification import StandardPackageSpecification
from models.customer_interaction.package_specification_interface import PackageSpecificationInterface


class ImperialPackageAdapter(PackageSpecificationInterface):
    """
    The ImperialPackageAdapter class converts imperial package specifications
    to metric specifications to comply with the system's standard.
    """

    def __init__(self, imperial_package):
        """
        Initialize the ImperialPackageAdapter.

        Args:
            imperial_package (ImperialPackageSpecification): The package specifications in imperial units.
        """
        self.imperial_package = imperial_package
        self.standard_spec = StandardPackageSpecification(
            width=imperial_package.width_in * 2.54,  # Convert inches to cm
            length=imperial_package.length_in * 2.54,
            height=imperial_package.height_in * 2.54,
            weight=imperial_package.weight_lb * 0.453592  # Convert pounds to kg
        )

    def get_weight(self):
        """
        Retrieve the package weight in kilograms.

        Returns:
            float: The package weight in kilograms.
        """
        return self.standard_spec.get_weight()  # Returns weight in kg

    def get_dimensions(self):
        """
        Retrieve the package dimensions in centimeters.

        Returns:
            list: A list of dimensions (width, length, height) in centimeters.
        """
        return self.standard_spec.get_dimensions()  # Returns dimensions in cm
