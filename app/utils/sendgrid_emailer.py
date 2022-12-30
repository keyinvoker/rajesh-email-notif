from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app import app_logger, error_logger
from app.config import (
    BASE_ENDPOINT,
    EMAIL_SENDER,
    SENDGRID_API_KEY,
)
from app.models.customer import Customer


def send_email_with_sendgrid(cust_id):
    customer = (
            Customer.query
            .filter_by(id=cust_id)
            .first()
    )

    subject = f'''\
Reminder {customer.notifs_received} for {customer.name}\
'''
    recipient = customer.email

    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=recipient,
        subject=subject,
        html_content=f'''
            <p>Reminder count: {customer.notifs_received + 1}</p>
            <p>Click the button below to stop notifs.</p>
            <form action="
                        {BASE_ENDPOINT}/verify/{customer.id}"
                        method="POST">
                <input type="submit" value="I understand." style="
                        border: 1px solid darkgreen;
                        color: whitesmoke;
                        background-color: green;">
            </form>
            '''
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        app_logger.info(
            'Email sent with SendGrid:',
            response.status_code,
            response.body,
            response.headers
        )
    except Exception as e:
        error_logger.exception(e)

    customer.notifs_received += 1
    customer.update()
