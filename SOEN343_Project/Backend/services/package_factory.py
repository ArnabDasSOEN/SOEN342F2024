from models.logistics.package import Package, FragilePackage
from models.customer_interaction.package_item import PackageItem
from models.customer_interaction.imperial_package_specification import ImperialPackageSpecification
from models.customer_interaction.metric_package_specification import MetricPackageSpecification
from models.logistics.adapters.imperial_package_adapter import ImperialPackageAdapter
from models.logistics.adapters.metric_package_adapter import MetricPackageAdapter
from dbconnection import db


class PackageFactory:
    @staticmethod
    def create_package(package_data: dict) -> Package:
        unit_system = package_data.pop("unit_system", "metric")
        is_fragile = package_data.get("is_fragile", False)
        package_items_data = package_data.pop("package_items", [])

        # Use appropriate adapter based on unit system
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

        db.session.add(package_spec)
        db.session.commit()

        # Create package instance based on fragility
        package = FragilePackage(package_specification_id=package_spec.id) if is_fragile else Package(
            package_specification_id=package_spec.id)
        db.session.add(package)
        db.session.commit()

        # Add items to package
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
