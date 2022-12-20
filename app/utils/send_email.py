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

from app.resources.rajesh_notif_task_individual import (
    RajeshEmailNotifIndividual
)

# supp = 'lol'


# class MyClass:
#     subject = f'''\
# Reminder Testing String Length {supp}\
# '''

with app.app_context():
    def send_email(customer, duration):
        context = ssl.create_default_context()
        em = EmailMessage()
        em['From'] = EMAIL_SENDER

        recipient = customer['email']

        subject = f'''\
    Reminder {customer['notifs_received']} for {customer['name']}\
    '''

        body = (
            f'''\
    <p>Reminder count: {customer['notifs_received']}</p>
    <p>On duration: <b>{duration}</b></p>
    <p>Click the button below to stop notifs.</p>
    <form action="
                {BASE_ENDPOINT}/verify/{customer['id']}"
                method="POST">
        <input type="submit" value="I understand." style="
                border: 1px solid darkgreen;
                color: whitesmoke;
                background-color: green;">
    </form>
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

            del em

        customer['notifs_received'] += 1
        updated_cust = (
            Customer.query
            .filter_by(id=customer['id'])
            .first()
        )
        updated_cust.notifs_received = customer['notifs_received']
        updated_cust.update()

        RajeshEmailNotifIndividual().get(
            RajeshEmailNotifIndividual, updated_cust.id
        )

        # TODO: remove current job from job list
