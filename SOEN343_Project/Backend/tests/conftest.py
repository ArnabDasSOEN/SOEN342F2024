# conftest.py
import pytest
from app import create_app
from dbconnection import db
from dotenv import load_dotenv
# Import ask_chatbot
from controller.customer_interaction_controller.chatbot_controller import chatbot_blueprint, ask_chatbot


@pytest.fixture
def session_state():
    # Return a fresh session state for each test
    return {}


@pytest.fixture
def client(session_state):
    load_dotenv()
    app = create_app(testing=True)  # Adjust to your app creation method
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Override `ask_chatbot` in the blueprint to use the provided `session_state`
    chatbot_blueprint.view_functions['ask_chatbot'] = lambda: ask_chatbot(
        session_state_override=session_state)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()
