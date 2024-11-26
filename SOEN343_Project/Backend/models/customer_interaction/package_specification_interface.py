"""
This module defines the PackageSpecificationInterface class, an abstract base class
for specifying the interface of package specifications, including methods for
retrieving weight and dimensions.
"""

from abc import ABC, abstractmethod


class PackageSpecificationInterface(ABC):
    """
    PackageSpecificationInterface is an abstract base class that enforces the implementation
    of methods for retrieving package weight and dimensions in derived classes.
    """

    @abstractmethod
    def get_weight(self):
        """
        Retrieve the weight of the package.

        Returns:
            float: The weight of the package.
        """
        pass

    @abstractmethod
    def get_dimensions(self):
        """
        Retrieve the dimensions of the package.

        Returns:
            list: A list of dimensions (e.g., width, length, height).
        """
        pass
