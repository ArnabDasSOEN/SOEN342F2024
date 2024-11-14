# blueprints.py

from controller.Customer_Interaction_Controller.delivery_request_controller import delivery_request_blueprint
from controller.logistics_controller.payment_controller import payment_blueprint
from controller.logistics_controller.delivery_controller import delivery_agent_blueprint
# Import the new auth blueprint
from controller.Customer_Interaction_Controller.user_controller import auth_blueprint


def register_blueprints(app):
    # Registers under /delivery_request
    app.register_blueprint(delivery_request_blueprint)
    # Registers under /payment
    app.register_blueprint(payment_blueprint)
    # Registers under /delivery_agent
    app.register_blueprint(delivery_agent_blueprint)
    # Registers under /auth
    app.register_blueprint(auth_blueprint)  # Register the auth blueprint
