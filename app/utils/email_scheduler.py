import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# from app.config import (
#     CHANGING_DURATION,
#     CONSTANT_DURATION,
#     PERIOD,
# )
# from app.resources.rajesh_notif_task import RajeshEmailNotif

scheduler = BackgroundScheduler(daemon=True)


# def banana():
#     print("scheduler: BANANA!")


# scheduler.add_job(
#     banana, trigger="interval", minutes=1
# )


# if PERIOD == "minutely":
#     scheduler.add_job(
#         RajeshEmailNotif().get, trigger="interval", minutes=DURATION
#     )

# elif PERIOD == "hourly":
#     scheduler.add_job(
#         RajeshEmailNotif().get, trigger="interval", hours=DURATION
#     )

# elif PERIOD == "daily":
#     Runs on Monday at 9:00 (am)
#     scheduler.add_job(
#         RajeshEmailNotif().get, 'cron', day_of_week='mon', hour=9, minute=00
#     )

#     scheduler.add_job(
#         RajeshEmailNotif().get, trigger="interval", days=DURATION
#     )

# elif PERIOD == "weekly":
#     scheduler.add_job(
#         RajeshEmailNotif().get, trigger="interval", weeks=DURATION
#     )

def start_scheduler():
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
