# Models/Logistics/Package.py
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from dbconnection import db


class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    package_specification_id = db.Column(
        db.Integer, db.ForeignKey('standard_package_specifications.id'))

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
        return False


class FragilePackage(Package):
    __tablename__ = 'fragile_packages'
    id = db.Column(db.Integer, db.ForeignKey('packages.id'), primary_key=True)
    fragile_handling_instructions = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'fragile_package'
    }

    @property
    def is_fragile(self) -> bool:
        return True
