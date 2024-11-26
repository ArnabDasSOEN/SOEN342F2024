import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import limiter  # Import limiter from extensions
from dbconnection import db
from blueprints import register_blueprints
from config import Config, TestConfig
from dotenv import load_dotenv

# Import facades and services
from facades.delivery_request_facade import DeliveryRequestFacade
from facades.order_facade import OrderFacade
from facades.payment_facade import PaymentFacade
from services.event_dispatcher import EventDispatcher
from services.quotation_service import QuotationService


def create_app(testing=False):
    load_dotenv()  # Load environment variables from .env
    # Enable instance-relative config
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # Load configuration
    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    # Initialize extensions
    limiter.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    register_blueprints(app)

    with app.app_context():
        print("Resolved Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

        db.create_all()

        # Initialize services and facades
        event_dispatcher = EventDispatcher()
        quotation_service = QuotationService()
        payment_facade = PaymentFacade(event_dispatcher)
        order_facade = OrderFacade()
        delivery_request_facade = DeliveryRequestFacade()

        def handle_payment_successful(event_data):
            order_facade.finalize_order(event_data["order_id"])

        event_dispatcher.add_listener(
            "payment_successful", handle_payment_successful)

        # Store facades in app config
        app.config['payment_facade'] = payment_facade
        app.config['order_facade'] = order_facade
        app.config['delivery_request_facade'] = delivery_request_facade

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
