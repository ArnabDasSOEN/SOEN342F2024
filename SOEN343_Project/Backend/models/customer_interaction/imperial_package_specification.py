"""
This module defines the ImperialPackageSpecification class, which represents
package dimensions and weight in imperial units (inches and pounds).
"""


class ImperialPackageSpecification:
    """
    The ImperialPackageSpecification class encapsulates package dimensions and weight
    in imperial units (inches and pounds).
    """

    def __init__(self, width_in, length_in, height_in, weight_lb):
        """
        Initialize an instance of ImperialPackageSpecification.

        Args:
            width_in (float): Width of the package in inches.
            length_in (float): Length of the package in inches.
            height_in (float): Height of the package in inches.
            weight_lb (float): Weight of the package in pounds.
        """
        self.width_in = width_in
        self.length_in = length_in
        self.height_in = height_in
        self.weight_lb = weight_lb

    def get_imperial_dimensions(self):
        """
        Retrieve the package dimensions in inches.

        Returns:
            list: A list containing the width, length, and height in inches.
        """
        return [self.width_in, self.length_in, self.height_in]

    def get_imperial_weight(self):
        """
        Retrieve the package weight in pounds.

        Returns:
            float: The package weight in pounds.
        """
        return self.weight_lb
