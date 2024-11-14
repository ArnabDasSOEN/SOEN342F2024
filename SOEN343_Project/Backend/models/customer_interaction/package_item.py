from dbconnection import db


class PackageItem(db.Model):
    __tablename__ = 'package_items'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey(
        'packages.id'), nullable=False)
    item_description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
