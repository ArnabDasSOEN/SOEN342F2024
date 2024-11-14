import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from dbconnection import db
from blueprints import register_blueprints
from config import Config, TestConfig

# Import facades and services
from facades.delivery_request_facade import DeliveryRequestFacade
from facades.order_facade import OrderFacade
from facades.payment_facade import PaymentFacade
from services.event_dispatcher import EventDispatcher
from services.quotation_service import QuotationService

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Load different configurations for testing or production
if os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Ensure tables are created within the application context
with app.app_context():
    db.create_all()

    # Initialize event dispatcher
    event_dispatcher = EventDispatcher()

    # Initialize services
    quotation_service = QuotationService()

    # Initialize facades
    payment_facade = PaymentFacade(event_dispatcher)
    order_facade = OrderFacade()
    delivery_request_facade = DeliveryRequestFacade()

    # Add the event listener for order creation
    def handle_payment_successful(event_data):
        order_facade.finalize_order(event_data["order_id"])

    event_dispatcher.add_listener(
        "payment_successful", handle_payment_successful
    )

    # Store facades in app config
    app.config['payment_facade'] = payment_facade
    app.config['order_facade'] = order_facade
    # Add this line
    app.config['delivery_request_facade'] = delivery_request_facade

# Register blueprints for routing
register_blueprints(app)

# Define a home route


@app.route('/')
def home():
    return "Welcome to the Flask application!"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
