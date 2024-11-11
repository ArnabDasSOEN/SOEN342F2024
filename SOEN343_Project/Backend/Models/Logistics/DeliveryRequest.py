from dbconnection import db
from Models.Customer_Interaction.address import Address


class DeliveryRequest(db.Model):
    __tablename__ = 'delivery_requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    package_details = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Requested")

    # Foreign keys to Address table
    pick_up_address_id = db.Column(
        db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    drop_off_address_id = db.Column(
        db.Integer, db.ForeignKey('addresses.id'), nullable=False)

    # Relationships to Address
    pick_up_address = db.relationship(
        "Address", foreign_keys=[pick_up_address_id], backref="pickup_requests")
    drop_off_address = db.relationship(
        "Address", foreign_keys=[drop_off_address_id], backref="dropoff_requests")

    def __init__(self, customer_id, package_details, status="Requested"):
        self.customer_id = customer_id
        self.package_details = package_details
        self.status = status
