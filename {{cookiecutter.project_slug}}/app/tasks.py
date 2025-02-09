from app.celery_worker import celery_app


@celery_app.task(name="app.tasks.multiply")
def multiply(x, y):
    return x * y
