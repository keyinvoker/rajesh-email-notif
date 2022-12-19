from app import app
from app.utils import email_scheduler

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
