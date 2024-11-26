"""
Package Update Service
Handles updates to packages, including their specifications and associated items.
"""

from models.logistics.package import Package
from models.customer_interaction.package_item import PackageItem
from models.customer_interaction.imperial_package_specification import ImperialPackageSpecification
from models.customer_interaction.metric_package_specification import MetricPackageSpecification
from models.logistics.adapters.imperial_package_adapter import ImperialPackageAdapter
from models.logistics.adapters.metric_package_adapter import MetricPackageAdapter
from dbconnection import db


class PackageUpdateService:
    """
    Service class for updating package details and associated items.
    """

    @staticmethod
    def update_package(package_id: int, package_data: dict) -> Package:
        """
        Updates the package details, including its specifications and items.

        Args:
            package_id (int): The ID of the package to update.
            package_data (dict): The updated package data.

        Returns:
            Package: The updated package instance.

        Raises:
            ValueError: If the package is not found.
        """
        # Retrieve the existing package
        package = Package.query.get(package_id)
        if not package:
            raise ValueError("Package not found")

        # Update package specifications
        unit_system = package_data.get("unit_system", "metric")
        is_fragile = package_data.get("is_fragile", package.is_fragile)

        if unit_system == "imperial":
            imperial_spec = ImperialPackageSpecification(
                width_in=package_data["width"],
                length_in=package_data["length"],
                height_in=package_data["height"],
                weight_lb=package_data["weight"]
            )
            package_spec = ImperialPackageAdapter(imperial_spec).standard_spec
        else:
            metric_spec = MetricPackageSpecification(
                width_cm=package_data["width"],
                length_cm=package_data["length"],
                height_cm=package_data["height"],
                weight_kg=package_data["weight"]
            )
            package_spec = MetricPackageAdapter(metric_spec).standard_spec

        # Persist the updated package specification
        db.session.add(package_spec)
        db.session.commit()

        # Update the package's specification ID and fragility
        package.package_specification_id = package_spec.id
        package.is_fragile = is_fragile
        db.session.commit()

        # Update package items
        PackageUpdateService.update_package_items(
            package, package_data.get("package_items", []))

        return package

    @staticmethod
    def update_package_items(package: Package, package_items_data: list):
        """
        Updates the items associated with a package.

        Args:
            package (Package): The package instance to update items for.
            package_items_data (list): A list of item data dictionaries.

        Returns:
            None
        """
        # Remove existing items associated with the package
        PackageItem.query.filter_by(package_id=package.id).delete()

        # Add new items
        for item_data in package_items_data:
            item = PackageItem(
                package_id=package.id,
                item_description=item_data["item_description"],
                quantity=item_data["quantity"],
                weight=item_data["weight"]
            )
            db.session.add(item)

        db.session.commit()
