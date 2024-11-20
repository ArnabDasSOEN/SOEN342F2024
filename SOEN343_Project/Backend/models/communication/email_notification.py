import os
import requests
from .notification import Notification
from dbconnection import db


class EmailNotification(Notification):
    __tablename__ = 'email_notifications'
    id = db.Column(db.Integer, db.ForeignKey(
        'notifications.id'), primary_key=True)
    email = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'email_notification'
    }

    def __init__(self, email, message_content, order_id):
        super().__init__(message_content, order_id=order_id)
        self.email = email

    def send_email(self):
        """
        Use Mailgun API to send the email.
        """
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")

        if not mailgun_api_key or not mailgun_domain:
            raise Exception("Mailgun API key or domain not configured")

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": f"Delivery Service <mailgun@{mailgun_domain}>",
                    "to": "testerstests06@gmail.com",
                    "subject": "Order Status Update",
                    "text": self.message_content,
                }
            )

            # Check if the email was sent successfully
            if response.status_code == 200:
                return True
            else:
                print(f"Mailgun API Error: {
                      response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return False

    def update(self, state: str):
        """
        Update the state and send the email notification.
        """
        self.message_content = f"Your order status is now {state}"
        self.status = "Pending"

        # Attempt to send the email
        if self.send_email():
            self.status = "Sent"
        else:
            self.status = "Failed"

        # Save the updated status in the database
        db.session.add(self)
        db.session.commit()
        print(f"Email to testerstests06@gmail.com: {self.status}")
