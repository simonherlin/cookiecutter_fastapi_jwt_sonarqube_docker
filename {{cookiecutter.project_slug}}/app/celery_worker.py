from celery import Celery

# Configuration Celery
celery_app = Celery(
    "worker",
    backend="redis://localhost:6379/0",  # Backend pour stocker les résultats
    broker="redis://localhost:6379/0",   # Broker pour les files d'attente
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "default"},
}

@celery_app.task(name="app.tasks.example_task")
def example_task(x, y):
    return x + y
