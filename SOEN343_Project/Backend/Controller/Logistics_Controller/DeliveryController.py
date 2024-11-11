from Models.Logistics.DeliveryRequest import DeliveryRequest
from dbconnection import db


class DeliveryController:
    def get_delivery_request_by_id(self, delivery_request_id):
        print(f"Retrieving DeliveryRequest {delivery_request_id}")
        return DeliveryRequest.query.filter_by(id=delivery_request_id).first()

    def create_delivery_request(self, customer_id, package_details, pick_up_data, drop_off_data):
        # Create pick-up and drop-off addresses
        pick_up_address = self.create_address(**pick_up_data)
        drop_off_address = self.create_address(**drop_off_data)

        # Create DeliveryRequest with the address IDs
        new_request = DeliveryRequest(
            customer_id=customer_id,
            package_details=package_details,
            status="Requested"
        )
        new_request.pick_up_address_id = pick_up_address.id
        new_request.drop_off_address_id = drop_off_address.id

        db.session.add(new_request)
        db.session.commit()

        return new_request

    def assign_delivery_agent(self, order):
        print("Assigning delivery agent to order")
        return "Agent_123"

    def notify_customer_with_tracking(self, customer, tracker):
        print(f"Notifying {customer} with tracker info: {tracker}")
