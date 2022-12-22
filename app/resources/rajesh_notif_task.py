from datetime import datetime, timedelta

from flask_restful import Resource

from app import app
from app.config import (
    CHANGING_DURATION,
    CONSTANT_DURATION,
    MAX,
    PERIOD,
)
from app.models.customer import Customer
from app.utils.email_scheduler import scheduler
from app.utils.emailer import send_email


class RajeshEmailNotif(Resource):
    def get(self):
        with app.app_context():
            cust_list = Customer.query.order_by(Customer.id).all()

            scheduled_customers_list = list()

            for cust in cust_list:

                print(f"\nWorking on Customer {cust.id}\n")

                notifs_received = cust.notifs_received
                schedule = datetime.now()

                while notifs_received < MAX:
                    print(notifs_received, " < ", MAX)

                    try:
                        duration = CHANGING_DURATION[notifs_received]
                    except Exception:
                        duration = CONSTANT_DURATION

                    if PERIOD == 'minutes':
                        duration = timedelta(minutes=duration)
                    elif PERIOD == 'hours':
                        duration = timedelta(hours=duration)
                    elif PERIOD == 'days':
                        duration = timedelta(days=duration)
                    elif PERIOD == 'weeks':
                        duration = timedelta(weeks=duration)

                    schedule += duration
                    schedule_string = schedule.strftime('%Y-%m-%d %H:%M:%S')
                    schedule_name = f'{cust.name} -- {schedule_string}'

                    scheduler.add_job(
                        send_email,
                        'date',
                        run_date=schedule_string,
                        name=schedule_name,
                        args=[cust.id]
                    )

                    notifs_received += 1

                    scheduled_customers_list.append(cust.name)

                cust.status = 'Inactive'
                cust.update()

            print("\nJobs:")
            for job in scheduler.get_jobs():
                print(job.id, ':', job)
            print("")

            return {'list': scheduled_customers_list}
