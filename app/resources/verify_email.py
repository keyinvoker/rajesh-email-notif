from flask_restful import Resource

from app import app
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerSchema


class VerifyEmail(Resource):
    # NOTE: User presses button on email -> update the data so notifs can stop
    def post(self, customer_id):
        with app.app_context():
            customer = Customer.query.filter_by(id=customer_id).first()
            customer.status = 'Active'
            customer.notifs_received = 0
            customer.update()
            customer_schema = CustomerSchema().dump(customer)
        return customer_schema
