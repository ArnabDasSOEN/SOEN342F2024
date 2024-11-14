from dbconnection import db


class StandardPackageSpecification(db.Model):
    __tablename__ = 'standard_package_specifications'

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Float, nullable=False)
    length = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __init__(self, width, length, height, weight):
        self.width = width
        self.length = length
        self.height = height
        self.weight = weight

    def get_weight(self):
        return self.weight

    def get_dimensions(self):
        return [self.width, self.length, self.height]
