import smtplib
import ssl
from email.message import EmailMessage
from flask_restful import Resource

from app.config import (
    ENDPOINT,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_SENDER,
    EMAIL_SERVER,
    MAX,
)
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerSchema
from app import app

context = ssl.create_default_context()
em = EmailMessage()
em['From'] = EMAIL_SENDER


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
                    cust['status'] == 'Unnotified'
                    and cust['notifs_received'] < MAX
                ):
                    recipient = cust['email']
                    subject = f"Reminder for {cust['name']}"
                    em['To'] = recipient
                    em['Subject'] = subject

                    cust['notifs_received'] += 1
                    updated_cust = (
                        Customer.query
                        .filter_by(id=cust['id'])
                        .first()
                    )
                    updated_cust.notifs_received = cust['notifs_received']
                    updated_cust.update()
                    cust_list.append(updated_cust.name)
                    body = (
                        f'''
                        <p>Reminder count: {cust['notifs_received']}</p>
                        <p>Click the button below to stop notifs.</p>
                        <form action="
                                    {ENDPOINT}/verify/{cust['id']}"
                                    method="POST">
                            <input type="submit" value="I understand." style="
                                    border: 1px solid darkgreen;
                                    color: whitesmoke;
                                    background-color: green;">
                        </form>
                        '''
                    )

                    em.set_content(body, subtype='html')

                    with smtplib.SMTP_SSL(
                        EMAIL_SERVER,
                        EMAIL_PORT,
                        context=context
                    ) as smtp:

                        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                        smtp.sendmail(EMAIL_SENDER, recipient, em.as_string())

                    del em['To']
                    del em['Subject']

                elif cust['notifs_received'] >= MAX:
                    updated_cust = (
                        Customer.query
                        .filter_by(id=cust['id'])
                        .first()
                    )
                    updated_cust.status = 'Inactive'
                    updated_cust.update()

            return {'list': cust_list}
