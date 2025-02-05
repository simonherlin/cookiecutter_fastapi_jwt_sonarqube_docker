from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas import user as user_schema

router = APIRouter()


@router.get("/me", response_model=user_schema.User)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/")
def read_users():
    return [
        {"user_id": 1, "name": "Alice"},
        {"user_id": 2, "name": "Bob"}
    ]
