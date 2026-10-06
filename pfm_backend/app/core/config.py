import os
import secrets
import warnings
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        secret = os.getenv("SECRET_KEY")
        if not secret:
            # Nessuna SECRET_KEY in ambiente: si genera una chiave effimera
            # invece di usare un default noto (che in produzione sarebbe un buco).
            secret = secrets.token_hex(32)
            warnings.warn(
                "SECRET_KEY non impostata: ne e' stata generata una effimera, "
                "i token non sopravvivono al riavvio. Impostala in .env.",
                RuntimeWarning,
            )
        self.SECRET_KEY = secret
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))
        )
        self.REFRESH_TOKEN_EXPIRE = timedelta(
            days=int(os.getenv("REFRESH_TOKEN_DAYS", "7"))
        )


settings = Settings()
