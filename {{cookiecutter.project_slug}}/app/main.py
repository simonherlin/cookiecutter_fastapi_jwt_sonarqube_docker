from fastapi import FastAPI
from app.api.router import router as api_router

app = FastAPI(title="{{ cookiecutter.project_name }} API")

# Inclusion du routeur centralisé
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
