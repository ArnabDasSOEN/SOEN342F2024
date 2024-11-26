from controller.customer_interaction_controller.delivery_request_controller import delivery_request_blueprint
from controller.logistics_controller.payment_controller import payment_blueprint
from controller.logistics_controller.delivery_controller import delivery_agent_blueprint
from controller.customer_interaction_controller.user_controller import auth_blueprint

# Import Chatbot blueprint
from controller.customer_interaction_controller.chatbot_controller import chatbot_blueprint


def register_blueprints(app):
    # Registers delivery request functionality
    app.register_blueprint(delivery_request_blueprint)
    # Registers payment functionality
    app.register_blueprint(payment_blueprint)
    # Registers delivery agent functionality
    app.register_blueprint(delivery_agent_blueprint)
    # Registers user authentication functionality
    app.register_blueprint(auth_blueprint)
    # Registers admin-specific functionality
    # app.register_blueprint(admin_auth_blueprint)
    # Registers delivery agent-specific authentication
   # app.register_blueprint(delivery_agent_auth_blueprint)
    # Registers chatbot functionality
    app.register_blueprint(chatbot_blueprint)  # Add chatbot routes
