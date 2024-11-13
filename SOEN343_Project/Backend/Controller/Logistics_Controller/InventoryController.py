from Models.Logistics.Inventory import Inventory
from dbconnection import db
from flask import jsonify


class InventoryController:
    def create_inventory(self, inventoryID, stockCount):
        new_inventory = Inventory(
            inventoryID=inventoryID,
            stockCount=stockCount
        )

        db.session.add(new_inventory)
        db.session.commit()

        return new_inventory
    
    def get_inventory_by_id(self, inventory_id):
        inventory = Inventory.query.get(inventory_id)

        if not inventory:
            return jsonify({"message": "Inventory not found"}), 404
        
        return jsonify({
            "id": inventory.id,
            "inventoryID": inventory.inventoryID,
            "stockCount": inventory.stockCount
        })
    
    def get_all_inventory(self):
        inventories = Inventory.query.all()

        return jsonify([{
            "id": inventory.id,
            "inventoryID": inventory.inventoryID,
            "stockCount": inventory.stockCount
        } for inventory in inventories])
    
    def update_inventory(self, inventory_id, stockCount):
        inventory = Inventory.query.get(inventory_id)

        if not inventory:
            return jsonify({"message": "Inventory not found"}), 404
        if stockCount is not None:
            inventory.stockCount = stockCount
        
        db.session.commit()
        return jsonify({"message": "Inventory updated successfully"})
    
    def delete_inventory(self, inventory_id):
        inventory = Inventory.query.get(inventory_id)
        
        if not inventory:
            return jsonify({"message": "Inventory not found"}), 404
        
        db.session.delete(inventory)
        db.session.commit()
        return jsonify({"message": "Inventory deleted successfully"})
    
    def update_stock_count(self, inventory_id, amount):
        inventory = Inventory.query.get(inventory_id)

        if not inventory:  
            return jsonify({"message": "Inventory not found"}), 404
        
        inventory.stockCount += amount
        db.session.commit()
        return jsonify({
            "message": "Stock count updated successfully",
            "new stock count": inventory.stockCount
            }), 200
        
