from datetime import datetime, timedelta
from typing import Any, Union

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..database import SessionLocal
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

from backend.common.config import get_settings
settings = get_settings()
SECRET_KEY = settings.secret_key if hasattr(settings, "secret_key") else "dev"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    settings.access_token_expire_minutes
    if hasattr(settings, "access_token_expire_minutes")
    else 60
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str) -> Union[models.User, None]:
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict[str, Any], roles: list[str] | None = None, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    to_encode.update({"roles": roles or []})
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
