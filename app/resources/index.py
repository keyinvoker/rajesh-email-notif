from flask_restful import Resource

# from app.utils.email_scheduler import scheduler

# import smtplib
# import ssl
# from email.message import EmailMessage

# from app.config import (
#     EMAIL_PASSWORD,
#     EMAIL_PORT,
#     EMAIL_SENDER,
#     EMAIL_SERVER,
# )

# context = ssl.create_default_context()
# em = EmailMessage()
# em['From'] = EMAIL_SENDER


# def fruit(fruit):
#     recipient = "joeriochandra@gmail.com"
#     subject = f"Fruit: {fruit}"

#     em['To'] = recipient
#     em['Subject'] = subject

#     body = (
#         '''
#         <p style="color: purple;">Test Doank!</p>
#         '''
#     )
#     em.set_content(body, subtype='html')

#     with smtplib.SMTP_SSL(
#         EMAIL_SERVER,
#         EMAIL_PORT,
#         context=context
#     ) as smtp:

#         smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         smtp.sendmail(EMAIL_SENDER, recipient, em.as_string())

#         del em['To']
#         del em['Subject']


class Index(Resource):
    def get(self):
        # scheduler.add_job(
        #     lambda: fruit('banana'),
        #     trigger='interval',
        #     minutes=1
        # )

        return {
            'app_desc': 'this app sends email notifs'
        }
