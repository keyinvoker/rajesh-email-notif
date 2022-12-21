import atexit
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(daemon=True)


def start_scheduler():
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
