from models.customer_interaction.standard_package_specification import StandardPackageSpecification
from models.customer_interaction.package_specification_interface import PackageSpecificationInterface
from models.customer_interaction.metric_package_specification import MetricPackageSpecification


class MetricPackageAdapter(PackageSpecificationInterface):
    def __init__(self, metric_package):
        self.metric_package = metric_package
        self.standard_spec = StandardPackageSpecification(
            width=metric_package.width_cm,
            length=metric_package.length_cm,
            height=metric_package.height_cm,
            weight=metric_package.weight_kg
        )

    def get_weight(self):
        return self.standard_spec.get_weight()  # Returns weight in kg

    def get_dimensions(self):
        return self.standard_spec.get_dimensions()  # Returns dimensions in cm
