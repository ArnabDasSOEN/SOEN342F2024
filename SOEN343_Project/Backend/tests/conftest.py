import pytest
from app import create_app
from dbconnection import db


@pytest.fixture
def client():
    app = create_app(testing=True)  # Adjust to your app creation method
    # In-memory test DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()
