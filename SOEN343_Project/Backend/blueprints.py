# blueprints.py

from Controller.Customer_Interaction_Controller.delivery_request_controller import delivery_request_blueprint
from Controller.Logistics_Controller.payment_controller import payment_blueprint
from Controller.Logistics_Controller.delivery_controller import delivery_agent_blueprint
# Import the new auth blueprint
from Controller.Customer_Interaction_Controller.user_controller import auth_blueprint
from Controller.Customer_Interaction_Controller.admin_controller import admin_auth_blueprint
from Controller.Customer_Interaction_Controller.delivery_agent_controller import delivery_agent_auth_blueprint


def register_blueprints(app):
    # Registers under /delivery_request
    app.register_blueprint(delivery_request_blueprint)
    # Registers under /payment
    app.register_blueprint(payment_blueprint)
    # Registers under /delivery_agent
    app.register_blueprint(delivery_agent_blueprint)
    # Registers under /auth
    app.register_blueprint(auth_blueprint)  # Register the auth blueprint
    # Registers under /admin_auth
    app.register_blueprint(admin_auth_blueprint)  # Register the admin_auth blueprint
    # Registers under /delivery_agent_auth
    app.register_blueprint(delivery_agent_auth_blueprint)  # Register the delivery_agent_auth blueprint
