from models.customer_interaction.standard_package_specification import StandardPackageSpecification


class ImperialPackageSpecification:
    def __init__(self, width_in, length_in, height_in, weight_lb):
        self.width_in = width_in
        self.length_in = length_in
        self.height_in = height_in
        self.weight_lb = weight_lb

    def get_imperial_dimensions(self):
        return [self.width_in, self.length_in, self.height_in]

    def get_imperial_weight(self):
        return self.weight_lb
