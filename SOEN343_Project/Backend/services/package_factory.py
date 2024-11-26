"""
Package Factory
Handles the creation of packages and their associated items and specifications.
"""

from models.logistics.package import Package, FragilePackage
from models.customer_interaction.package_item import PackageItem
from models.customer_interaction.imperial_package_specification import ImperialPackageSpecification
from models.customer_interaction.metric_package_specification import MetricPackageSpecification
from models.logistics.adapters.imperial_package_adapter import ImperialPackageAdapter
from models.logistics.adapters.metric_package_adapter import MetricPackageAdapter
from dbconnection import db


class PackageFactory:
    """
    A factory class for creating package instances with associated specifications and items.
    """

    @staticmethod
    def create_package(package_data: dict) -> Package:
        """
        Creates a package with its specification and associated items.

        Args:
            package_data (dict): A dictionary containing package details, including dimensions,
                                 weight, unit system, items, and whether it is fragile.

        Returns:
            Package: The created Package or FragilePackage instance.
        """
        # Extract unit system and package fragility
        unit_system = package_data.pop("unit_system", "metric")
        is_fragile = package_data.get("is_fragile", False)
        package_items_data = package_data.pop("package_items", [])

        # Create and adapt package specification based on the unit system
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

        # Persist the package specification to the database
        db.session.add(package_spec)
        db.session.commit()

        # Create the package (fragile or standard) and persist it
        package = FragilePackage(package_specification_id=package_spec.id) if is_fragile else Package(
            package_specification_id=package_spec.id
        )
        db.session.add(package)
        db.session.commit()

        # Add items to the package
        for item_data in package_items_data:
            item = PackageItem(
                package_id=package.id,
                item_description=item_data["item_description"],
                quantity=item_data["quantity"],
                weight=item_data["weight"]
            )
            db.session.add(item)

        db.session.commit()
        return package
