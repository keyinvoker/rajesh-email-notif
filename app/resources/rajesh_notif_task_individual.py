
from flask_restful import Resource

from app import app
from app.config import (
    MAX,
    CHANGING_DURATION,
    CONSTANT_DURATION,
)
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerSchema
from app.utils.email_scheduler import scheduler

from app.utils.send_email import send_email


class RajeshEmailNotifIndividual(Resource):

    # NOTE: Function to sweep check users' status
    def get(self, customer_id):
        with app.app_context():
            customer = Customer.query.filter_by(id=customer_id).first()

            if (
                customer.status != 'Inactive'
                and customer.notifs_received < MAX
            ):

                # TODO: MASUKKIN FUNCTION SEND_EMAIL DISINI!!!
                #     - cocokin value 'notifs_received' ke array
                #       CHANGING_DURATION (per element)
                try:
                    duration = CHANGING_DURATION[customer.notifs_received]
                except Exception:
                    duration = CONSTANT_DURATION

                cust = CustomerSchema().dump(customer)
                print(f"""\
[scheduler added]: {cust['name']} - {cust['notifs_received']} - {duration}\
""")
                scheduler.add_job(
                    lambda: send_email(cust, duration),
                    trigger="interval",
                    minutes=duration
                )  # TODO: scheduler overwrites prev schedules when stacked
                # TODO: remove job(?) when done

            elif customer.notifs_received >= MAX:
                customer.status = 'Inactive'
                customer.update()

        return {'list': 'list'}
