import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    # Configuration JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "a_very_secret_key_change_me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        env_file = ".env"


settings = Settings()
