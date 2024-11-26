from faker import Faker
from dbconnection import db
from models.customer_interaction.delivery_agent import DeliveryAgent
from werkzeug.security import generate_password_hash
from app import create_app  # Import the app factory function

# Initialize Faker
fake = Faker()


def create_random_delivery_agents(num_agents=5):
    for _ in range(num_agents):
        name = fake.name()
        password = generate_password_hash("password", method='pbkdf2:sha256')
        email = fake.unique.email()
        phone_number = fake.phone_number()

        delivery_agent = DeliveryAgent(
            name=name,
            password=password,
            email=email,
            phone_number=phone_number
        )

        db.session.add(delivery_agent)

    db.session.commit()
    print(f"Added {num_agents} random delivery agents to the database.")


if __name__ == "__main__":
    # Use the app factory to create the app instance
    app = create_app()
    with app.app_context():
        create_random_delivery_agents(10)
