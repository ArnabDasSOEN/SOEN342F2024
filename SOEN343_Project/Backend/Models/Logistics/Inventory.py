from dbconnection import db

class Inventory:
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    inventoryID = db.Column(db.String(50), nullable=False)
    stockCount = db.Column(db.Integer, nullable=False)

    def __init__(self, inventoryID, stockCount):
        self.inventoryID = inventoryID
        self.stockCount = stockCount
