# blueprints.py
from Controller.Customer_Interaction_Controller.user_controller import user_blueprint
from Controller.Logistics_Controller.OrderController import order_blueprint
# Import additional blueprints here as the application grows


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(order_blueprint, url_prefix='/order')
