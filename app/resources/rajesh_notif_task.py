
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


class RajeshEmailNotif(Resource):

    # NOTE: Function to sweep check users' status
    def get(self):
        with app.app_context():
            customers = Customer.query.all()
            customer_schema = CustomerSchema(many=True)
            output = customer_schema.dump(customers)

            cust_list = list()

            for cust in output:
                if (
                    cust['status'] != 'Inactive'
                    and cust['notifs_received'] < MAX
                ):

                    try:
                        duration = CHANGING_DURATION[cust['notifs_received']]
                    except Exception:
                        duration = CONSTANT_DURATION

                    print(f"""\
[scheduler added]: {cust['name']} - {cust['notifs_received']} - {duration}\
""")
                    scheduler.add_job(
                        lambda: send_email(cust, duration),
                        trigger="interval",
                        minutes=duration
                    )  # TODO: scheduler overwrites prev schedules when stacked

                    cust_list.append(cust['name'])

                elif cust['notifs_received'] >= MAX:
                    updated_cust = (
                        Customer.query
                        .filter_by(id=cust['id'])
                        .first()
                    )
                    updated_cust.status = 'Inactive'
                    updated_cust.update()
            print(scheduler.get_jobs())
            return {'list': cust_list}
