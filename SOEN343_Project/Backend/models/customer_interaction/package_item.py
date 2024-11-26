"""
This module defines the PackageItem class, which represents individual items
within a package, including their description, quantity, and weight.
"""

from dbconnection import db


class PackageItem(db.Model):
    """
    PackageItem represents an individual item in a package, including
    its description, quantity, and weight. It is associated with a package.
    """

    __tablename__ = 'package_items'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey(
        'packages.id'), nullable=False)
    item_description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    # pylint: disable=too-few-public-methods
