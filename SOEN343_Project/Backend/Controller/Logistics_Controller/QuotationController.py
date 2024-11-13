from Models.Customer_Interaction.Quotation import Quotation
from dbconnection import db
from flask import jsonify

class QuotationController:

    @staticmethod
    def create_quotation(price, quotationID):
        new_quotation = Quotation(price=price, quotationID=quotationID)
        db.session.add(new_quotation)
        db.session.commit()
        return jsonify({"message": "Quotation created successfully!"}), 201
    
    @staticmethod
    def get_quotations(quotation_id):
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return jsonify({"error": "Quotation not found!"}), 404
        
        return jsonify({
            "id": quotation.id,
            "price": quotation.price,
            "quotationID": quotation.quotationID
        }), 200
    
    @staticmethod
    def get_all_quotations():
        quotations = Quotation.query.all()
        return jsonify([{
            "id": q.id,
            "price": q.price,
            "quotationID": q.quotationID
        } for q in quotations]), 200
    
    @staticmethod
    def update_quotation(quotation_id, price=None, quotationID=None):
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return jsonify({"error": "Quotation not found!"}), 404
        
        if price is not None:
            quotation.price = price

        if quotationID is not None:
            quotation.quotationID = quotationID

        db.session.commit()
        return jsonify({"message": "Quotation updated successfully!"}), 200
    
    @staticmethod
    def delete_quotation(quotation_id):
        quotation = Quotation.query.get(quotation_id)
        if not quotation:
            return jsonify({"error": "Quotation not found!"}), 404
        
        db.session.delete(quotation)
        db.session.commit()
        return jsonify({"message": "Quotation deleted successfully!"}), 200
    
    @staticmethod
    def calculate_quotation():
        # Simulate quotation calculation logic
        # For example, calculate the price based on the delivery address, weight, and delivery method
        return jsonify({"message": "Quotation calculated successfully!"}), 200