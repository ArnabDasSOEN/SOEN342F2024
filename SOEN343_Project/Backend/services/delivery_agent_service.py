# services/delivery_agent_service.py

from models.customer_interaction.delivery_agent import DeliveryAgent
from dbconnection import db
import random


class DeliveryAgentService:
    @staticmethod
    def assign_delivery_agent():
        # Retrieve a list of available delivery agents (modify criteria as needed)
        delivery_agents = db.session.query(
            DeliveryAgent).all()  # Adjust criteria if necessary
        if delivery_agents:
            # Randomly select one delivery agent
            return random.choice(delivery_agents)
        else:
            print("No available delivery agents.")
            return None
