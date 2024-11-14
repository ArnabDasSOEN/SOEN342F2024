from models.customer_interaction.standard_package_specification import StandardPackageSpecification
from models.customer_interaction.package_specification_interface import PackageSpecificationInterface
from models.customer_interaction.imperial_package_specification import ImperialPackageSpecification


class ImperialPackageAdapter(PackageSpecificationInterface):
    def __init__(self, imperial_package):
        self.imperial_package = imperial_package
        self.standard_spec = StandardPackageSpecification(
            width=imperial_package.width_in * 2.54,  # Convert inches to cm
            length=imperial_package.length_in * 2.54,
            height=imperial_package.height_in * 2.54,
            weight=imperial_package.weight_lb * 0.453592  # Convert pounds to kg
        )

    def get_weight(self):
        return self.standard_spec.get_weight()  # Returns weight in kg

    def get_dimensions(self):
        return self.standard_spec.get_dimensions()  # Returns dimensions in cm
