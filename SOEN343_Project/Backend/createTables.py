# createTables.py
from app import app
from dbconnection import db
from Models.Customer_Interaction.user import User
from Models.Customer_Interaction.admin import Admin
from Models.Customer_Interaction.customer import Customer
from Models.Customer_Interaction.deliveryAgent import DeliveryAgent

with app.app_context():
    db.drop_all()  # Be careful; this deletes all tables
    db.create_all()  # Recreates tables with the updated schema
