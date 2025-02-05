from fastapi import APIRouter
from {{ cookiecutter.project_slug }}.app.api.endpoints import auth, user

router = APIRouter()

# Inclusion des routeurs définis dans le dossier endpoints
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
