# blueprints.py
from Controller.Customer_Interaction_Controller.user_controller import user_blueprint
# Import additional blueprints here as the application grows


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/user')
    # Register additional blueprints here
