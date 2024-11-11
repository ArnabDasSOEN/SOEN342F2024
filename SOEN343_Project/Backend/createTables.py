from app import app
from dbconnection import db
from Models.Customer_Interaction.user import User
from Models.Customer_Interaction.admin import Admin
from Models.Customer_Interaction.customer import Customer
from Models.Customer_Interaction.deliveryAgent import DeliveryAgent
from Models.Logistics.Order import Order
from Models.Logistics.Tracker import Tracker

with app.app_context():
    db.drop_all()  # Drops all tables (be careful with this in production)
    db.create_all()  # Creates tables as defined in the models
