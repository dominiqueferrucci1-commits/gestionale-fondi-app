from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(user_id: int, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    if token_type == "access":
        expire = now + settings.ACCESS_TOKEN_EXPIRE
    elif token_type == "refresh":
        expire = now + settings.REFRESH_TOKEN_EXPIRE
    else:
        raise ValueError("token_type deve essere 'access' o 'refresh'")
    payload = {"sub": str(user_id), "type": token_type, "iat": now, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None