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
# from app.utils.emailer import send_email


import atexit
import smtplib
import ssl
from email.message import EmailMessage

from app.config import (
    BASE_ENDPOINT,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_SENDER,
    EMAIL_SERVER,
)


class RajeshEmailNotif(Resource):

    # NOTE: Function to sweep check users' status
    def get(self):
        with app.app_context():
            cust_list = Customer.query.order_by(Customer.id).all()

            scheduled_customers_list = list()

            for cust in cust_list:

                print(f"\nWorking on Customer {cust.id}\n")

                def _func():
                    send_email(cust.id)

                notifs_received = cust.notifs_received
                schedule = datetime.now()

                while notifs_received < MAX:

                    try:
                        duration = CHANGING_DURATION[notifs_received]
                    except Exception:
                        duration = CONSTANT_DURATION

                    if PERIOD == 'minutes':
                        # duration = timedelta(minutes=duration)
                        duration = timedelta(seconds=duration)
                    elif PERIOD == 'hours':
                        duration = timedelta(hours=duration)
                    elif PERIOD == 'days':
                        duration = timedelta(days=duration)
                    elif PERIOD == 'weeks':
                        duration = timedelta(weeks=duration)

                    schedule += duration
                    schedule_string = schedule.strftime('%Y-%m-%d %H:%M:%S')
                    schedule_name = f'{cust.name} -- {schedule_string}'

                    print(
                        f"Passing on {cust.name} -> ID: {cust.id}"
                    )

                    scheduler.add_job(
                        send_email,
                        # _func,
                        'date',
                        run_date=schedule_string,
                        name=schedule_name,
                        args=[cust.id]
                    )

                    notifs_received += 1

                    scheduled_customers_list.append(cust.name)

            print("\nJobs:")
            for job in scheduler.get_jobs():
                print(job.id, ':', job)
            print("")

            # scheduler.start()
            # atexit.register(lambda: scheduler.shutdown())

            return {'list': scheduled_customers_list}


def send_email(cust_id):
    with app.app_context():
        context = ssl.create_default_context()
        em = EmailMessage()
        em['From'] = EMAIL_SENDER

        customer = (
            Customer.query
            .filter_by(id=cust_id)
            .first()
        )

        print(
            f"""
Working on {customer.name} -> {customer.id} (passed ID: {cust_id})
"""
        )

        recipient = customer.email

        subject = f'''\
Reminder {customer.notifs_received} for {customer.name}\
'''

        body = (
            f'''\
            <p>Reminder count: {customer.notifs_received}</p>
            <p>Click the button below to stop notifs.</p>
            <form action="
                        {BASE_ENDPOINT}/verify/{customer.id}"
                        method="POST">
                <input type="submit" value="I understand." style="
                        border: 1px solid darkgreen;
                        color: whitesmoke;
                        background-color: green;">
            </form>\
            '''
        )

        em['To'] = recipient
        em['Subject'] = subject
        em.set_content(body, subtype='html')

        with smtplib.SMTP_SSL(
            EMAIL_SERVER,
            EMAIL_PORT,
            context=context
        ) as smtp:

            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, recipient, em.as_string())

        customer.notifs_received += 1
        customer.update()

        print("\nUpdated Jobs:")
        for job in scheduler.get_jobs():
            print(job)
        print("")
