import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import (
    DURATION,
    PERIOD,
)
from app.resources.rajesh_notif_task import RajeshEmailNotif

scheduler = BackgroundScheduler(daemon=True)

if PERIOD == "minutely":
    scheduler.add_job(
        func=RajeshEmailNotif().get, trigger="interval", minutes=DURATION
    )

elif PERIOD == "hourly":
    scheduler.add_job(
        func=RajeshEmailNotif().get, trigger="interval", hours=DURATION
    )

elif PERIOD == "daily":
    scheduler.add_job(
        func=RajeshEmailNotif().get, trigger="interval", days=DURATION
    )

    # Runs on Monday at 9:00 (am)
    # scheduler.add_job(
    #     RajeshEmailNotif().get, 'cron', day_of_week='mon', hour=9, minute=00
    # )

elif PERIOD == "weekly":
    scheduler.add_job(
        func=RajeshEmailNotif().get, trigger="interval", weeks=DURATION
    )

scheduler.start()
atexit.register(lambda: scheduler.shutdown())
