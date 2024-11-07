# tests/conftest.py
import pytest
from app import app, db


@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    # Use in-memory database for faster tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Set up the database
    with app.app_context():
        db.create_all()

    # Create a test client
    with app.test_client() as client:
        yield client

    # Clean up the database
    with app.app_context():
        db.drop_all()
