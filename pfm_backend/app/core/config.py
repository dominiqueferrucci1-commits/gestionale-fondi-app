import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-cambiami-in-produzione")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE: timedelta = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))
    )
    REFRESH_TOKEN_EXPIRE: timedelta = timedelta(
        days=int(os.getenv("REFRESH_TOKEN_DAYS", "7"))
    )


settings = Settings()