import schedule

from app.config import PERIOD
from app.resources.rajesh_notif_task import RajeshEmailNotif


def rajesh_mailer():
    RajeshEmailNotif.get(RajeshEmailNotif)


schedule.every(PERIOD).day.at("09:00").do(rajesh_mailer)

while True:
    schedule.run_pending()
