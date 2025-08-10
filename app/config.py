# from pydantic import BaseSettings
from pydantic_settings import BaseSettings  # ✅ Correct for v2

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:091003@localhost:5432/DigitalCheckList"
    SECRET_KEY: str = "yoursecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
