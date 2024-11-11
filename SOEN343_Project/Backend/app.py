import os
from flask import Flask
from dbconnection import db
from blueprints import register_blueprints
from config import Config, TestConfig

# Import controllers and OrderFacade
from Controller.Logistics_Controller.PaymentController import PaymentController
from Controller.Logistics_Controller.DeliveryController import DeliveryController
from Controller.Logistics_Controller.OrderController import OrderController
from Models.Logistics.OrderFacade import OrderFacade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

    # Initialize controllers
    payment_controller = PaymentController()
    delivery_controller = DeliveryController()
    order_controller = OrderController()

    # Create an instance of OrderFacade with the controllers
    order_facade = OrderFacade(
        payment_controller, delivery_controller, order_controller)

    # Make order_facade accessible via app.config
    app.config['order_facade'] = order_facade

register_blueprints(app)


@app.route('/')
def home():
    return "Welcome to the Flask application!"


if __name__ == '__main__':
    app.run(debug=True)
