"""
Delivery Agent Service Module
Handles operations related to assigning delivery agents.
"""

import random
from models.customer_interaction.delivery_agent import DeliveryAgent
from dbconnection import db


class DeliveryAgentService:
    """
    Service class for managing delivery agent-related operations.
    """

    @staticmethod
    def assign_delivery_agent() -> DeliveryAgent:
        """
        Assigns a delivery agent from the list of available agents.

        Returns:
            DeliveryAgent: A randomly selected delivery agent if available.
            None: If no delivery agents are available.
        """
        # Retrieve a list of all available delivery agents (adjust query criteria as needed)
        delivery_agents = db.session.query(DeliveryAgent).all()

        if delivery_agents:
            # Randomly select one delivery agent
            return random.choice(delivery_agents)

        print("No available delivery agents.")
        return None
