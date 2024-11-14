from app import app
from dbconnection import db

with app.app_context():
    db.drop_all()  # Drops all tables (be careful with this in production)
    db.create_all()  # Creates tables as defined in the models
