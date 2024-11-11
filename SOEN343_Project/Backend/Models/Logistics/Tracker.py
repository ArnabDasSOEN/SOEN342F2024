from dbconnection import db


class Tracker(db.Model):
    __tablename__ = 'trackers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    delivery_agent_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="In Transit")

    order = db.relationship("Order", backref="tracker")

    def __init__(self, order_id, delivery_agent_id, status="In Transit"):
        self.order_id = order_id
        self.delivery_agent_id = delivery_agent_id
        self.status = status
