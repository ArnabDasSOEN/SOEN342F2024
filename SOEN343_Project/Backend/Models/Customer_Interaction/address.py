from dbconnection import db


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.String(10), nullable=False)
    apartment_number = db.Column(db.String(10), nullable=True)
    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __init__(self, street, house_number, apartment_number, postal_code, city, country):
        self.street = street
        self.house_number = house_number
        self.apartment_number = apartment_number
        self.postal_code = postal_code
        self.city = city
        self.country = country
