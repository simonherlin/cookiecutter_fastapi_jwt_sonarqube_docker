from fastapi import APIRouter
from app.api.endpoints import auth, user

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
