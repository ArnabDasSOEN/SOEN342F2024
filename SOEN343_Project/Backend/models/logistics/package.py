from sqlalchemy.orm import relationship
from dbconnection import db


class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    package_specification_id = db.Column(
        db.Integer, db.ForeignKey('standard_package_specifications.id'))
    package_specification = db.relationship('StandardPackageSpecification')

    # Relationship to PackageItems
    items = db.relationship('PackageItem', backref='package',
                            lazy=True, cascade="all, delete-orphan")

    # Polymorphic setup for inheritance
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'package',
        'polymorphic_on': type
    }

    @property
    def is_fragile(self) -> bool:
        """Default fragility property."""
        return False

    def calculate_volumetric_weight(self) -> float:
        """
        Calculate the volumetric weight based on dimensions (cm).
        Formula: (L * W * H) / 5000
        """
        dimensions = self.package_specification.get_dimensions()
        length, width, height = dimensions
        return (length * width * height) / 5000

    def calculate_total_weight(self) -> float:
        """
        Calculate the total weight, including package items.
        """
        spec_weight = self.package_specification.get_weight()
        items_weight = sum(item.weight * item.quantity for item in self.items)
        return spec_weight + items_weight

    def calculate_shipping_weight(self) -> float:
        """
        Determine the shipping weight as the maximum of volumetric or total weight.
        """
        volumetric_weight = self.calculate_volumetric_weight()
        total_weight = self.calculate_total_weight()
        return max(volumetric_weight, total_weight)


class FragilePackage(Package):
    __tablename__ = 'fragile_packages'
    id = db.Column(db.Integer, db.ForeignKey('packages.id'), primary_key=True)
    fragile_handling_instructions = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'fragile_package'
    }

    @property
    def is_fragile(self) -> bool:
        """Override fragility property."""
        return True
