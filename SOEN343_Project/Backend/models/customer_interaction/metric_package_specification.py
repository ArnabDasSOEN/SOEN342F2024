from models.customer_interaction.standard_package_specification import StandardPackageSpecification


class MetricPackageSpecification:
    def __init__(self, width_cm, length_cm, height_cm, weight_kg):
        self.width_cm = width_cm
        self.length_cm = length_cm
        self.height_cm = height_cm
        self.weight_kg = weight_kg

    def get_metric_dimensions(self):
        return [self.width_cm, self.length_cm, self.height_cm]

    def get_metric_weight(self):
        return self.weight_kg
