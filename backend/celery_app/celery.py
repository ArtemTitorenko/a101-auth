from celery import Celery

from core.config import CELERY_BROKER_URL


app = Celery("celery_app", broker=CELERY_BROKER_URL)

app.autodiscover_tasks()


@app.task
def debug():
    print("debug")


if __name__ == "__main__":
    app.start()
