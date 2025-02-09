from fastapi import FastAPI
from app.celery_worker import celery_app
from app.api.router import router as api_router

app = FastAPI(title="{{ cookiecutter.project_name }} API")

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/task/{x}/{y}")
def run_task(x: int, y: int):
    task = celery_app.send_task("app.tasks.example_task", args=[x, y])
    return {"task_id": task.id}
