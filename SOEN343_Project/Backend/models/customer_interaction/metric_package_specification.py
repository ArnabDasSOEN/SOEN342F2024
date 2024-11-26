"""
This module defines the MetricPackageSpecification class, which represents
package dimensions and weight in metric units (centimeters and kilograms).
"""


class MetricPackageSpecification:
    """
    The MetricPackageSpecification class encapsulates package dimensions and weight
    in metric units (centimeters and kilograms).
    """

    def __init__(self, width_cm, length_cm, height_cm, weight_kg):
        """
        Initialize a MetricPackageSpecification instance.

        Args:
            width_cm (float): Width of the package in centimeters.
            length_cm (float): Length of the package in centimeters.
            height_cm (float): Height of the package in centimeters.
            weight_kg (float): Weight of the package in kilograms.
        """
        self.width_cm = width_cm
        self.length_cm = length_cm
        self.height_cm = height_cm
        self.weight_kg = weight_kg

    def get_metric_dimensions(self):
        """
        Retrieve the package dimensions in centimeters.

        Returns:
            list: A list containing the width, length, and height in centimeters.
        """
        return [self.width_cm, self.length_cm, self.height_cm]

    def get_metric_weight(self):
        """
        Retrieve the package weight in kilograms.

        Returns:
            float: The package weight in kilograms.
        """
        return self.weight_kg
