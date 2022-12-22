from app import api
from app.resources.rajesh_notif_task import RajeshEmailNotif
from app.resources.verify_email import VerifyEmail

api.add_resource(RajeshEmailNotif, '/notif')
api.add_resource(VerifyEmail, '/verify/<int:customer_id>')
