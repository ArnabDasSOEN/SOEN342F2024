from faker import Faker
from dbconnection import db
from models.customer_interaction.delivery_agent import DeliveryAgent
from werkzeug.security import generate_password_hash
from app import app  # Import your Flask app

# Initialize Faker
fake = Faker()


def create_random_delivery_agents(num_agents=5):
    for _ in range(num_agents):
        # Generate random data for each agent
        name = fake.name()
        # Use pbkdf2:sha256 as the hashing method
        password = generate_password_hash("password", method='pbkdf2:sha256')
        email = fake.unique.email()
        phone_number = fake.phone_number()

        # Create DeliveryAgent instance
        delivery_agent = DeliveryAgent(
            name=name,
            password=password,
            email=email,
            phone_number=phone_number
        )

        # Add to session
        db.session.add(delivery_agent)

    # Commit all agents to the database
    db.session.commit()
    print(f"Added {num_agents} random delivery agents to the database.")


# Run the function with application context
if __name__ == "__main__":
    with app.app_context():  # Use the application context
        create_random_delivery_agents(10)  # Generate 10 agents for example
