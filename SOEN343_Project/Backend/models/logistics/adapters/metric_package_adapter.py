"""
This module provides the MetricPackageAdapter class, which adapts metric package
specifications to the standard package specification interface.
"""

from ..customer_interaction.standard_package_specification import StandardPackageSpecification
from ..customer_interaction.package_specification_interface import PackageSpecificationInterface


class MetricPackageAdapter(PackageSpecificationInterface):
    """
    The MetricPackageAdapter class adapts a MetricPackageSpecification to the
    standard package specification interface.
    """

    def __init__(self, metric_package):
        """
        Initialize the MetricPackageAdapter.

        Args:
            metric_package (MetricPackageSpecification): The package specifications in metric units.
        """
        self.metric_package = metric_package
        self.standard_spec = StandardPackageSpecification(
            width=metric_package.width_cm,
            length=metric_package.length_cm,
            height=metric_package.height_cm,
            weight=metric_package.weight_kg
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
