import requests
import os
from .notification import Notification
from dbconnection import db


class SMSNotification(Notification):
    __tablename__ = 'sms_notifications'
    id = db.Column(db.Integer, db.ForeignKey(
        'notifications.id'), primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'sms_notification'
    }

    def __init__(self, phone_number, message_content, order_id):
        super().__init__(message_content, order_id=order_id)
        self.phone_number = phone_number

    def send_sms(self):
        """
        Use Textbelt API to send the SMS.
        """
        textbelt_api_key = os.getenv("TEXTBELT_API_KEY")
        if not textbelt_api_key:
            raise Exception(
                "Textbelt API key not configured in environment variables")

        try:
            # Make the Textbelt API request
            response = requests.post(
                "https://textbelt.com/text",
                data={
                    "phone": self.phone_number,
                    "message": self.message_content,
                    "key": textbelt_api_key,
                }
            )
            response_data = response.json()
            return response_data.get("success", False)
        except requests.RequestException as e:
            print(f"Textbelt error: {e}")
            return False

    def update(self, state: str):
        """
        Update the state and send the SMS notification.
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
