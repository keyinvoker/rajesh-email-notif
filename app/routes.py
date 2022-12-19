from app import api
from app.resources.rajesh_notif_task import RajeshEmailNotif

api.add_resource(RajeshEmailNotif, '/notif')
