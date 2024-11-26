"""
This module defines the SMSNotification class for sending SMS notifications
using the Textbelt API and interacting with the database.
"""

import os  # Standard library import
import requests  # Third-party import
from dbconnection import db  # First-party import
from .notification import Notification  # Local import


class SMSNotification(Notification):
    """
    SMSNotification handles SMS notification functionality, including
    sending messages via the Textbelt API and updating the notification state.
    """

    __tablename__ = 'sms_notifications'
    id = db.Column(db.Integer, db.ForeignKey(
        'notifications.id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'sms_notification'
    }

    def __init__(self, phone_number, message_content, order_id):
        """
        Initialize an SMSNotification instance with phone number, message, and order ID.

        Args:
            phone_number (str): The recipient's phone number.
            message_content (str): The message content.
            order_id (int): The associated order ID.
        """
        super().__init__(message_content, order_id=order_id)
        self.phone_number = phone_number

    def send_sms(self):
        """
        Use Textbelt API to send the SMS.

        Returns:
            bool: True if the SMS was sent successfully, False otherwise.
        """
        textbelt_api_key = os.getenv("TEXTBELT_API_KEY")
        if not textbelt_api_key:
            raise ValueError(
                "Textbelt API key not configured in environment variables")

        try:
            # Make the Textbelt API request
            response = requests.post(
                "https://textbelt.com/text",
                data={
                    "phone": self.phone_number,
                    "message": self.message_content,
                    "key": textbelt_api_key,
                },
                timeout=10  # Set an appropriate timeout value
            )
            response_data = response.json()
            return response_data.get("success", False)
        except requests.RequestException as e:
            print(f"Textbelt error: {e}")
            return False

    def update(self, state: str):
        """
        Update the state and send the SMS notification.

        Args:
            state (str): The new state of the order.
        """
        self.message_content = f"Your order status is now {state}"
        self.status = "Pending"

        # Attempt to send the SMS
        if self.send_sms():
            self.status = "Sent"
        else:
            self.status = "Failed"

        # Save the updated status in the database
        db.session.add(self)
        db.session.commit()
        print(f"SMS to {self.phone_number}: {self.status}")
