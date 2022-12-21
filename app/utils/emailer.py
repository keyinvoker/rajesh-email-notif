import smtplib
import ssl
from email.message import EmailMessage

from app import app
from app.models.customer import Customer
from app.config import (
    BASE_ENDPOINT,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_SENDER,
    EMAIL_SERVER,
)

from app.utils.email_scheduler import scheduler


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
            f"Working on {customer.name} -> {customer.id} (passed ID: {cust_id})"
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
