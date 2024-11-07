# app.py
"""
This module initializes the Flask application, sets up configurations,
and registers blueprints for the application routes.
"""
import os
from flask import Flask
from dbconnection import db  # Import db from extensions
# Import the blueprint registration function
from blueprints import register_blueprints
from config import Config, TestConfig

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)


db.init_app(app)  # Initialize db with app

with app.app_context():
    db.drop_all()
    db.create_all()  # This creates all tables


@app.route('/')
def home():
    """Return a welcome message for the Flask application."""
    return "Welcome to the Flask application!"


# Register all blueprints from the central function
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
