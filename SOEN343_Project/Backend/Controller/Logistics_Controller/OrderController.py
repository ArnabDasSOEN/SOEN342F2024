from flask import Blueprint, current_app, request, jsonify
from Models.Logistics.Order import Order
from Models.Logistics.Tracker import Tracker
from Models.Logistics.DeliveryRequest import DeliveryRequest
from Models.Customer_Interaction.deliveryAgent import DeliveryAgent
from dbconnection import db


class OrderController:
    def create_order(self, delivery_request_id, customer_id):
        # Create the Order with individual parameters
        order = Order(delivery_request_id=delivery_request_id,
                      customer_id=customer_id, status="Pending")
        db.session.add(order)
        db.session.commit()
        return order

    def assign_delivery_agent(self, order, delivery_agent):
        # Assume delivery_agent is a field on Order or manage this as per your schema
        order.delivery_agent = delivery_agent
        db.session.commit()

    def create_tracker(self, order, delivery_agent):
        tracker = Tracker(order_id=order.id,
                          delivery_agent_id=1)
        db.session.add(tracker)
        db.session.commit()
        return tracker

    def assign_tracker(self, order, tracker):
        order.tracker_id = tracker.id  # Adjust if there's a relationship in Order
        db.session.commit()


order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/process_order', methods=['POST'])
def process_order():
    data = request.json
    delivery_request_id = data.get('delivery_request_id')
    payment_method = data.get('payment_method')

    order_facade = current_app.config['order_facade']
    success = order_facade.process_payment_and_create_order(
        delivery_request_id, payment_method)

    if success:
        return jsonify({"status": "Order processed successfully"}), 200
    else:
        return jsonify({"status": "Order processing failed"}), 400
